
## Фото-сортировцик с созданием поддиректорий с датой создания, переворотом и обратным геокодированием на основе EXIF данных

Если имя файла имеет формат:
20210801_12121.jpg
IMG-20171007-WA1111.jpeg
IMG_20171006_1111.jpg
photo_111@24-03-2025_2222.jpg
и дата создания позднее, то в директорию берется дата из имени файла

``` bash
git clone https://github.com/SergeyMi37/photo-sorter
cd photo-sorter
```

Create virtual environment (optional)
``` bash
python3 -m venv env
source env/bin/activate
```

Create virtual environment for Windows
``` bash
python -m venv env
source env/Scripts/activate
```

Install all requirements:
``` bash
pip install -r requirements.txt
```

Укажите исходную и целевую директорию
``` bash
python selector-dirs-tk.py 
```

### Во время написания программы не один ИИ не пострадал, но потрепан был изрядно GigaChat (@gigachat_bot)
Его собрат GigaCode смотрелся не очень, но старался помогать в VsCode)


 Для сборки исполняемого файла (*.exe) вашей программы на Tkinter для Windows используется инструмент **PyInstaller**. Вот пошаговая инструкция по сборке релиза приложения:

### Шаги по созданию релиза

#### 1. Установка PyInstaller
Сначала убедитесь, что у вас установлен PyInstaller. Если нет, установите его командой:
```bash
pip install pyinstaller
```
[[4](https://habr.com/ru/sandbox/182102/)]

#### 3. Сборка с помощью PyInstaller
Откройте терминал и перейдите в папку вашего проекта. Затем выполните команду:
```bash
pyinstaller --onefile --windowed photosorter.py
```
Параметры команды:
- `--onefile`: Создает один файл `.exe`, содержащий всю необходимую библиотеку.
- `--windowed`: Запускает ваше приложение без консольного окна.

Это создаст два каталога: `build` и `dist`. В каталоге `dist` появится ваш исполняемый файл.

### Дополнительная настройка сборок

#### Настройка иконки приложения
Вы можете добавить свою иконку приложению, используя следующий формат:
```bash
pyinstaller --onefile --windowed --icon путь_до_иконки.ico имя_скрипта.py
```
Иконка должна иметь расширение `.ico`.

#### Добавление зависимых файлов
Если ваша программа зависит от внешних ресурсов (например, изображений или конфигурационных файлов), добавьте их следующим образом:
```bash
pyinstaller --onefile --windowed --add-data "путь_до_файла;название_каталога" имя_скрипта.py
```
Например, если у вас есть картинка `"logo.png"` в корне проекта, команда будет выглядеть так:
```bash
pyinstaller --onefile --windowed --icon doc/icon.ico --add-data "./doc/icon.ico;."  selector-dirs-tk.py
```
или
```bash
pip install auto-py-to-exe
pip install --update auto-py-to-exe
auto-py-to-exe
```

#### Тестирование конвертации дат из имени файла
```bash
pytest test_image_dates.py -v
```