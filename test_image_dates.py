from datetime import datetime
import pytest
from sorter import get_date_images

# Тестовые случаи
@pytest.mark.parametrize("filename, expected_date", [
    # Корректные форматы
    ("IMG-20171007-WA0001.jpeg", datetime(2017, 10, 7)),
    ("IMG-20171007-WA0001.jpeg", datetime(2017, 10, 7)),
    ("IMG_20171006_123456.jpg", datetime(2017, 10, 6)),
    ("20250804_125529.jpg", datetime(2025, 8, 4)),
    ("20231231_235959.jpg", datetime(2023, 12, 31)),
    ("photo_24-03-2025_123.jpg", datetime(2025, 3, 24)),
    ("photo_1111@24-03-2025_2222.jpg", datetime(2025, 3, 24)),
    
    # Некорректные данные (должны возвращать None)
    ("random_file.txt", None),
    ("photo_with_no_date.jpg", None),
    ("photo_invalid@date.jpg", None),
    ("photo_1234567890.jpg", None),  # Неправильный формат даты
    ("IMG-invalid", None),
    (None, None),  # None вместо строки
    (12345, None),  # Число вместо строки
])
def test_get_date_images(filename, expected_date):
    assert get_date_images(filename) == expected_date

@pytest.mark.parametrize("invalid_filename", [
    "IMG-20201301-WA0001.jpeg",  # Несуществующий месяц
    "IMG_20200230_123456.jpg",   # Несуществующий день
    "photo_32-01-2020_abc.jpg",  # Несуществующий день
    "photo_01-13-2020_xyz",      # Несуществующий месяц
    "photo_1111@32-01-2020_2222.jpg",  # Несуществующий день
])
def test_invalid_dates(invalid_filename):
    assert get_date_images(invalid_filename) is None