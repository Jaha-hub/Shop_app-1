import re

def validate_password(value) -> str:

    """
    Функция валидации пароля

    Пароль должен состоять из строчных и заглавных букв, цифр, и спец. симвалов
    :param value: значение пароля
    :return: значение пароля
    """

    if len(value) < 8:
        raise ValueError("Пароль должен состоять из 8 символов")
    if not re.search(r"[A-ZА-Я]", value):
        raise ValueError("Пароль должен состоять хотя бы из одной заглавной буквы")
    if not re.search(r"[a-zа-я]", value):
        raise ValueError("Пароль должен состоять хотя бы из одной строчной буквы")
    if not re.search(r"[0-9]", value):
        raise ValueError("Пароль должен состоять хотя бы из одной цифры")
    if not re.search(r"[\W_]", value):
        raise ValueError("Пароль должен состоять хотя бы из одного спец символа")
    return value