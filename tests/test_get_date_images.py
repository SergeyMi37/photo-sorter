import pytest
from datetime import datetime
from ..sorter import get_date_images

def test_get_date_images_img_dash(monkeypatch):
    """Тестирует корректное извлечение даты из имени файла с префиксом 'IMG-'."""
    
    def mock_strptime(date_string, format):
        assert date_string == '20171007'
        assert format == '%Y-%m-%d'
        return datetime(2017, 10, 7)
    
    monkeypatch.setattr('datetime.datetime.strptime', mock_strptime)
    result = get_date_images('IMG-20171007-WA.jpeg')
    assert result == datetime(2017, 10, 7)

def test_get_date_images_img_underscore(monkeypatch):
    """Тестирует корректное извлечение даты из имени файла с префиксом 'IMG_'."""
    
    def mock_strptime(date_string, format):
        assert date_string == '20171006'
        assert format == '%Y-%m-%d'
        return datetime(2017, 10, 6)
    
    monkeypatch.setattr('datetime.datetime.strptime', mock_strptime)
    result = get_date_images('IMG_20171006_123.jpg')
    assert result == datetime(2017, 10, 6)

def test_get_date_images_photo_jpg(monkeypatch):
    """Тестирует корректное извлечение даты из имени файла с префиксом 'photo_' и расширением .jpg."""
    
    def mock_strptime(date_string, format):
        assert date_string == '24-03-2025'
        assert format == '%d-%m-%Y'
        return datetime(2025, 3, 24)
    
    monkeypatch.setattr('datetime.datetime.strptime', mock_strptime)
    result = get_date_images('photo_24-03-2025_123.jpg')
    assert result == datetime(2025, 3, 24)

def test_get_date_images_photo_non_jpg(monkeypatch):
    """Тестирует извлечение даты из имени файла с префиксом 'photo_' без расширения .jpg."""
    
    def mock_strptime(date_string, format):
        assert date_string == '24-03-2025'
        assert format == '%d-%m-%Y'
        return datetime(2025, 3, 24)
    
    monkeypatch.setattr('datetime.datetime.strptime', mock_strptime)
    result = get_date_images('photo_24-03-2025_123.txt')
    assert result == datetime(2025, 3, 24)

def test_get_date_images_no_matching_prefix():
    """Тестирует случай, когда имя файла не соответствует ни одному из шаблонов."""
    
    result = get_date_images('test_file.jpg')
    assert result is None

def test_get_date_images_invalid_date_format(monkeypatch):
    """Тестирует обработку исключения при некорректном формате даты в имени файла."""
    
    def mock_strptime(*args, **kwargs):
        raise ValueError("Invalid date format")
    
    monkeypatch.setattr('datetime.datetime.strptime', mock_strptime)
    with pytest.raises(ValueError):
        get_date_images('IMG-20171007-WA.jpeg')

def test_get_date_images_invalid_date_value(monkeypatch):
    """Тестирует обработку исключения при невозможности разбора даты (например, 31 февраля)."""
    
    def mock_strptime(*args, **kwargs):
        raise ValueError("Invalid date value")
    
    monkeypatch.setattr('datetime.datetime.strptime', mock_strptime)
    with pytest.raises(ValueError):
        get_date_images('photo_31-02-2020.jpg')

def test_get_date_images_min_date(monkeypatch):
    """Тестирует извлечение минимальной допустимой даты."""
    
    min_date = datetime(1, 1, 1)
    
    def mock_strptime(date_string, format):
        assert date_string == '01-01-0001'
        assert format == '%d-%m-%Y'
        return min_date
    
    monkeypatch.setattr('datetime.datetime.strptime', mock_strptime)
    result = get_date_images('photo_01-01-0001_123.jpg')
    assert result == min_date

def test_get_date_images_max_date(monkeypatch):
    """Тестирует извлечение максимальной допустимой даты."""
    
    max_date = datetime(9999, 12, 31)
    
    def mock_strptime(date_string, format):
        assert date_string == '31-12-9999'
        assert format == '%d-%m-%Y'
        return max_date
    
    monkeypatch.setattr('datetime.datetime.strptime', mock_strptime)
    result = get_date_images('photo_31-12-9999_123.jpg')
    assert result == max_date