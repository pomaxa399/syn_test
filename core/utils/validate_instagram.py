import re


def validate_instagram_username(inst_username):
    # Регулярное выражение для валидации имени пользователя Instagram
    username_regex = r'^[a-zA-Z0-9](?!.*[_.]{2})[a-zA-Z0-9._]{0,28}[a-zA-Z0-9]$'

    # Проверка соответствия имени пользователя регулярному выражению
    if re.match(username_regex, inst_username):
        return inst_username
    else:
        return None


if __name__ == '__main__':
    # Примеры использования функции
    usernames = [
        "valid_username",
        "valid.username",
        "valid.username123",
        "valid_username_123",
        "invalid__username",
        "invalid..username",
        "invalid-username",
        "invalid username",
        "username_that_is_way_too_long_for_instagram"
    ]

    for username in usernames:
        if validate_instagram_username(username):
            print(f"'{username}' is a valid Instagram username.")
        else:
            print(f"'{username}' is not a valid Instagram username.")
