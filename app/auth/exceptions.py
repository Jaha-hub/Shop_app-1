from app.core.exceptions import Unauthorized, Conflict


class InvalidUsernamePassword(Unauthorized):
    """
    Ошибка username
    """

class InvalidToken(Unauthorized):
    """
    Ошибка невалидного токена
    """

class UsernameAlreadyExist(Conflict):
    """
    Имя пользователя уже занята
    """

class EmailAlreadyExist(Conflict):
    """
    Почта уже занята
    """