import re


def validate_phone_number(phone):
    # Убираем пробелы и лишние символы
    phone = phone.strip()

    # Регулярное выражение для проверки и удаления префикса +7
    pattern = r'^\+?7(\d{10})$'

    match = re.match(pattern, phone)
    if match:
        # Если номер соответствует шаблону, возвращаем номер без префикса
        return '7' + match.group(1)
    else:
        # Если номер не соответствует шаблону, возвращаем None
        return None
