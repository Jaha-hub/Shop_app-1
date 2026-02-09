from app.core.exceptions import Unauthorized, Conflict


class InvalidUsernamePassword(Unauthorized):
    """
    Ошибка юзернейма или пароля
    """

class InvalidToken(Unauthorized):
    """
    Ошибка невалидного токена
    """

class UsernameAlreadyExist(Conflict):
    """
    Имя пользователя уже занято
    """

class EmailAlreadyExist(Conflict):
    """
    Почта уже занята
    """

