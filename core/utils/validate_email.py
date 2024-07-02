import re


def validate_email(email):
    # Регулярное выражение для валидации email
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Проверка соответствия email регулярному выражению
    if re.match(email_regex, email):
        return email
    else:
        return None
    