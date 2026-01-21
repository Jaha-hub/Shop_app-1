from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import UserRegister, UserRead, ChengePasswordSchemas


class AuthManager:
    def __init__(
            self,
            session: AsyncSession,
    ):
        pass

    async def login(
            self,
            username: str,
            password: str,

    ):
        """
        Метод для входа в учёт запись

        проверяет наличие username в БД
        проверяет правильность пароль с БД

        :param username: имя пользователя
        :param password: пароль

        :return: Unauthorized: Ошибка авторизации

        :return: JWT token
        """
        pass

    async def register(
            self,
            request: UserRegister
    ):
        """
        Метод для регистрации пользователя

        проверят наличии username в БД

        проверяет наличие почты

        Хэширует пароль

        Создаёт пользователя в БД


        :param request: объект модельки
        :return: Моделька созданного пользователя
        """
        pass

    async def get_me(
            self,
            token: str,
    ) -> UserRead:
        """
        Метод для получение информации о пльзователи

        Проверяем токен на валидность

        Берём информацию по ИД из БД

        :param token: JWT token
        :return: Моделька пользователя
        """
        pass

    async def change_password(
            self,
            user_id: int,
            request: ChengePasswordSchemas,

    ):
        """
        Метод изменение пароля

        Проверка наличия пользователя

        проверяет старый пароль пользователя и хеширует новый пароль

        Изменяет пароль в БД



        :param user_id: ИД пользователя
        :param request: Моделька
        :return: ничего
        """
        pass

    async def refresh_token(
            self,
            token: str,

    ):
        """
        Метод для обновления токена

        Проверяет валидность токена

        Создаёт новую пару токенов

        :param token: JWT token
        :return: JWT token
        """
        pass




























