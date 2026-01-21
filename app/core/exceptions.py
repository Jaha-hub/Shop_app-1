class Unauthorized(Exception):
    """
    Ошибки связанны с аутификацией
    """


class Forbidden(Exception):
    """
    Ошибки связанны с павами
    """


class NotFound(Exception):
    """
    Вызывается когда не найден обьект
    """


class Conflict(Exception):
    """
    Конфликт
    """

class BadRequest(Exception):
    """
    Запрос не правильный
    """