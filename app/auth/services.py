from datetime import datetime, timedelta


from jose import jwt, JWTError
from passlib.hash import argon2

from app.auth.exceptions import InvalidToken
from app.core.settings import settings

class PasswordService:
    """
    Класс для работы с паролями
    """

    def hash(self, password: str) -> str:
        """
        Метод для шифровки указанного пароля

        :param password: пароль
        :return: зашифрованный пароль
        """
        return argon2.hash(
            password
        )



    def verify(self, password: str, hashed_password: str)-> bool:
        """
        Метод для проверки зашифрованного пароля

        :param password: введенный пароль
        :param hashed_password: зашифрованный пароль
        :return: true если пароль правильный иначе false
        """
        return argon2.verify(
            password,
            hashed_password
        )


class TokenService:
    """
    Класс для работы с токенами
    """

    def encode(
            self,
            sub: str,
            is_refresh: bool = False,
    ):
        """
        Метод для создания JWT токена

        :param sub: субъект для которого мы создаем токен(пользователь)
        :param is_refresh: флажок обозначающий создание refresh токена или access токена
        :return: JWT токен
        """
        exp = timedelta(minutes=settings.REFRESH_EXPIRES) if is_refresh else timedelta(minutes=settings.ACCESS_EXPIRES)
        payload = {
            'sub': sub,
            "is_refresh":is_refresh,
            "exp": datetime.now() + exp,
        }
        return jwt.encode(
            payload,
            algorithm=settings.TOKEN_ALGORITHM,
            key=settings.TOKEN_SECRET_KEY,
        )

    def decode(
            self,
            token: str
    ) -> dict:
        """
        Метод для расшифровывания токена

        :param token: JWT токен
        :return: payload, то есть информация о нашем субъекте
        """

        try:
            payload = jwt.decode(
                token,
                algorithms=[settings.TOKEN_ALGORITHM],
                key=settings.TOKEN_SECRET_KEY,

            )
        except JWTError:
            raise InvalidToken("Invalid Credentials")

        return payload
