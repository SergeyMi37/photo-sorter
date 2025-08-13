import os, datetime, pickle
from pathlib import Path
from PIL import Image
from geopy.geocoders import Nominatim
from PIL.ExifTags import TAGS
#from datetime import datetime

# Функция для получения даты из имени файла
def get_date_images(name):
    dat = None
    # IMG-20171007-WA*.jpeg
    if name.startswith('IMG-'):
        dat = datetime.datetime.strptime(name[4:14], '%Y%m%d')
    # IMG_20171006_*.jpg
    if name.startswith('IMG_'):
        dat = datetime.datetime.strptime(name[4:14], '%Y%m%d')
    # photo_*@24-03-2025_*.jpg
    if name.startswith('photo_'):
        if name.endswith('.jpg'):
            dat = datetime.datetime.strptime(name[6:16], '%d-%m-%Y')
        else:
            dat = datetime.datetime.strptime(name[6:16], '%d-%m-%Y')
    print(f'Дата: {dat}')
    return dat

# Функция для получения абсолютного пути изображения
def find_images(root_dir):
    """Ищет все изображения в корневой директории и возвращает путь"""
    extensions = ('*.jpg', '*.jpeg', '*.png', '*.bmp')
    return [path for ext in extensions for path in root_dir.rglob(ext)]

# Функция для вычисления правильного угла поворота
def compute_rotation_angle(exif_orientation):
    """
    Возвращает угол поворота для выравнивания изображения
    Основано на значении Orientation в EXIF
    """
    if exif_orientation == None:
        return 0
    elif exif_orientation == 1:
        return 0
    elif exif_orientation == 3:
        return 180
    elif exif_orientation == 6:
        return 270
    elif exif_orientation == 8:
        return 90
    else:
        raise ValueError(f"Неправильное значение orientation: {exif_orientation}")


def reverse_geocode(lat, lon):
    # Базовая ссылка API Nominatim
    base_url = 'https://nominatim.openstreetmap.org/reverse'
    # Параметры запроса
    params = {
        'format': 'json',       # Формат результата — JSON
        'lat': lat,             # Широта точки
        'lon': lon,             # Долгота точки
        'zoom': 18,             # Уровень детализации карты
        'addressdetails': 1     # Возвращение детальной адресной информации
    }
    headers = {'User-Agent': 'Mozilla/5.0'}
    #response = requests.get(url, headers=headers)
    try:
        response = requests.get(base_url, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            address = data['address']
            result = f"{address.get('road', '')}, {address.get('village', '')}, {address.get('city', '')}, {address.get('state', '')}, {address.get('country', '')}"
            return 200, result.strip(', ')
        else:
            return response.status_code, (f'Ошибка: {response.status_code}')

    except Exception as e:
        return 1, (f'Ошибка обработки запроса: {e}')

def sanitize_filename(s):
    """Очистка строки для использования в именах файлов/директорий и ограничим длину"""
    return ''.join(c if c.isalnum() or c in (' ', '.', '_', '-') else '_' for c in s).strip()[:50]

def convert_gps_to_decimal(gps_info):
    """
    Преобразует GPSInfo из EXIF в десятичные широту и долготу.
    
    :param gps_info: Словарь с данными GPS (например, {1: 'N', 2: (55, 48, 32.19156), ...})
    :return: Кортеж (широта, долгота) в десятичных градусах
    """
    # Получаем данные широты
    lat_deg, lat_min, lat_sec = gps_info[2]
    lat_dir = gps_info[1]
    
    # Вычисляем десятичную широту
    decimal_lat = lat_deg + (lat_min / 60) + (lat_sec / 3600)
    if lat_dir.upper() == 'S':
        decimal_lat = -decimal_lat
    
    # Получаем данные долготы
    lon_deg, lon_min, lon_sec = gps_info[4]
    lon_dir = gps_info[3]
    
    # Вычисляем десятичную долготу
    decimal_lon = lon_deg + (lon_min / 60) + (lon_sec / 3600)
    if lon_dir.upper() == 'W':
        decimal_lon = -decimal_lon
    
    return (decimal_lat, decimal_lon)


def exif_gps_to_decimal(exif_data):
    """
    Извлекает GPS-координаты из EXIF-данных и преобразует их в десятичный формат.
    
    :param exif_data: Словарь с EXIF-данными (включая 'GPSInfo')
    :return: Кортеж (широта, долгота) в десятичных градусах или None, если GPS-данных нет
    """
    if 'GPSInfo' not in exif_data:
        return None
    
    gps_info = exif_data['GPSInfo']
    
    # Проверяем наличие необходимых ключей
    required_keys = {1, 2, 3, 4}
    if not required_keys.issubset(gps_info.keys()):
        return None
    
    try:
        # Обрабатываем широту
        lat_dir = gps_info[1]
        lat_deg, lat_min, lat_sec = gps_info[2]
        decimal_lat = lat_deg + (lat_min / 60) + (lat_sec / 3600)
        if lat_dir.upper() == 'S':
            decimal_lat = -decimal_lat
        
        # Обрабатываем долготу
        lon_dir = gps_info[3]
        lon_deg, lon_min, lon_sec = gps_info[4]
        decimal_lon = lon_deg + (lon_min / 60) + (lon_sec / 3600)
        if lon_dir.upper() == 'W':
            decimal_lon = -decimal_lon
        
        return (float(decimal_lat), float(decimal_lon))
    
    except (TypeError, ValueError, IndexError):
        return None


def process_image(image_path, target_dir,mode='create', geo_cache=None, new_entries=0):
    msg = 'ok'
    try:
        image_path = Path(image_path)
        target_dir = Path(target_dir)
        
        # Чтение оригинальных метаданных файла
        orig_stat = os.stat(image_path)
        orig_create_time = orig_stat.st_ctime
        orig_modify_time = orig_stat.st_mtime
        
        # Открытие изображения и чтение EXIF
        img = Image.open(image_path)
        exif_dict = {}
        
        # Проверка наличия EXIF
        if hasattr(img, "_getexif"):
            exif_data = img._getexif()
            if exif_data:
                # Преобразование EXIF-данных в словарь
                exif_dict = {}
                for tag_id, value in exif_data.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    exif_dict[tag_name] = value
                
                # Определение ориентации и необходимого поворота
                rotation_angle = compute_rotation_angle(exif_dict.get("Orientation"))
                if rotation_angle != 0:
                    img = img.rotate(rotation_angle, expand=True)
        
        # Извлечение даты съёмки
        date_taken = exif_dict.get("DateTimeOriginal")
        
        # Если дата съёмки не указана, используем дату создания файла
        if not date_taken:
            try:
                # Получаем дату создания файла (ctime)
                file_creation_time = os.path.getctime(image_path)
                
                # Форматируем дату в формате "ГГГГ:ММ:ДД"
                date_taken = datetime.datetime.fromtimestamp(file_creation_time).strftime('%Y:%m:%d')
                #print(f"Используем дату файла: {date_taken} для {image_path}")
            except Exception as e:
                msg = f"Не удалось получить дату файла для {image_path}: {e}"
                print(msg)
                return msg, geo_cache, new_entries
        
        # Базовая структура директории
        base_folder = target_dir / date_taken[:10].replace(':', '-')
        address = ""        
        # Обработка геолокационных данных, если они существуют
        if mode=='geotag' and exif_dict.get("GPSInfo"):
            lat, lon = exif_gps_to_decimal(exif_dict)
            #print(lat,lon)
            if lat:
                try:
                    cache_key = f"{round(lat, 7)},{round(lon, 7)}"
                    #cache_key = f"{lat},{lon}"
                    #print(cache_key)
                    if cache_key in geo_cache:
                        address = geo_cache[cache_key]
                    else:
                        locator = Nominatim(user_agent="myGeocoder")
                        location = locator.reverse(cache_key)
                        address = sanitize_filename(location.address)
                        geo_cache[cache_key] = address
                        new_entries += 1
                        #print(address)
                        
                except Exception as geocode_err:
                    print(f"Ошибка геокодирования: {geocode_err}")        

        # Создание конечной директории с учётом адреса
        if address:
            fname = f"{date_taken[:10]}_{address.replace(' ', '_').replace('__', '_')}_{cache_key}"
            base_folder = target_dir / f"{fname.replace(':', '-')}" # Убираем двоеточия
            #print(output_folder)
        
        output_folder = base_folder        
        output_folder.mkdir(parents=True, exist_ok=True)
        
        # Финальный путь выходного файла
        final_output_path = output_folder / image_path.name
        
        # Сохранение обработанного изображения
        img.save(final_output_path)
        
        # Возвращаем исходные временные метаданные
        os.utime(final_output_path, (orig_create_time, orig_modify_time))
    
    except Exception as e:
        msg = f"Ошибка при обработке {image_path}: {e}"
        print(msg)
    return msg, geo_cache, new_entries

def photosorter(s,d,mode, progress_callback=None):
    # Имя файла для кэша
    CACHE_FILE = "photosorter_cache.pkl"
    # Загружаем кэш из файла, если он существует
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rb') as f:
            geo_cache = pickle.load(f)
    else:
        geo_cache = {}
    # Счётчик новых запросов
    new_entries = 0

    msg = 'ok'
    source_directory = Path(s)
    destination_directory = Path(d)
    if os.path.exists(source_directory):
        all_images = find_images(source_directory)
        if mode=='count':
            msg = f'Будет обработано {len(all_images)} файлов'
            return msg
        total_files = len(all_images)
        #for image_path in all_images:
        for i, image_path in enumerate(all_images, 1):
            res, geo_cache, new_entries = process_image(
                image_path, 
                destination_directory,
                mode=mode,
                geo_cache= geo_cache,
                new_entries= new_entries)
            # Обновляем прогресс
            if progress_callback:
                progress_callback(i, total_files)
        # Сохраняем кэш при завершении (если были изменения)
        if new_entries > 0:
            with open(CACHE_FILE, "wb") as f:
                pickle.dump(geo_cache, f)

    else:
        msg = (f'Директория {source_directory} не существует')
    return msg

# Основной блок программы
if __name__ == "__main__":
    source_directory = ("d:/_proj/_python/photo-sorter/source2/")
    destination_directory = ("d:/_proj/_python/photo-sorter/target/")
    photosorter(source_directory,destination_directory)
