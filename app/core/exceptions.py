class Unauthorized(Exception):
    """
    Вызывается когда у пользователя ошибка связанная с аутентификацией
    """


class Forbidden(Exception):
    """
    Вызывается когда у пользователя ошибка связанная с правами
    """


class NotFound(Exception):
    """
    Вызывается когда не бы найден объект
    """


class Conflict(Exception):
    """
    Вызывается когда случился конфликт
    """


class BadRequest(Exception):
    """
    Вызывается когда запрос был неправильный
    """


