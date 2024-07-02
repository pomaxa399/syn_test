import re
from datetime import datetime


def normalize_date(date_str):
    # Заменяем все возможные разделители на точки
    normalized_date = re.sub(r'[^\d]', '.', date_str)
    return normalized_date


def validate_date(date_str):
    # Преобразуем введенную строку в нормализованный формат
    normalized_date = normalize_date(date_str)

    # Проверяем правильность формата даты
    try:
        datetime.strptime(normalized_date, '%d.%m.%Y')
        return normalized_date
    except ValueError:
        return None

if __name__ == '__main__':
    # Примеры использования функции
    dates = [
        "27.02.1986",
        "27 02 1986",
        "27-02-1986",
        "27=02=1986",
        "27:02:1986",
        "27/02/1986"
    ]

    for date in dates:
        valid_date = validate_date(date)
        if valid_date:
            print(f"'{date}' is a valid date. Normalized: {valid_date}")
        else:
            print(f"'{date}' is not a valid date.")