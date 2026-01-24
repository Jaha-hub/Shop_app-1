from datetime import datetime, timedelta

from passlib.exc import InvalidTokenError
from passlib.hash import argon2
from jose import jwt, JWTError

from app.auth.exceptions import InvalidToken
from app.core.settings import settings

class PasswordServises:
    """

    """

    def hash(
            self,
            password: str
    ) -> str:
        """
        Метод будет шифровать Пароль


        :param password: Пароль
        :return: Шифрованный Пароль
        """

        return argon2.hash(
            password
        )

    def verify(
            self,
            password: str,
            heshed_password: str
    ) -> bool:
        """
        Метод Проверка ведённого пароля с зашифрованным

        :param password: Видённый пароль
        :param heshed_password: Зашифрованный пароль
        :return: True/False
        """

        return argon2.verify(
            password,
            heshed_password,
        )


class TokenServises:
    """
    Класс для работы с токеном
    """


    def encode(
            self,
            sub: str,
            is_refresh: bool = False,
    ):
        """
        Метод для создания jwt токена

        :param sub: Субъект Пользователя
        :param is_refresh: Вид токена
        :return: JWT Токен
        """
        exp = timedelta(minutes=settings.REFRESH_EXPIRES) if is_refresh else timedelta(minutes=settings.ACCESS_EXPIRES)

        payload = {
            'sub': sub,
            "is_refresh": is_refresh,
            "exp": datetime.now() + exp
        }
        return jwt.encode(
            payload,
            algorithm=settings.JWT_ALGORITHM,
            key= settings.JWT_SECRET_KEY,
        )

    def decode(
            self,
            token: str,
    ) -> dict:
        """
        Метод для расшифровки JWT токена

        :param token: JWT токен
        :return: Информация о Пользователе
        """
        try:
            payload = jwt.decode(
                token,
                algorithms=[settings.JWT_ALGORITHM],
                key=settings.JWT_SECRET_KEY,
            )
        except JWTError:
            raise InvalidToken(
                "Invalid token",
            )

        return payload






















