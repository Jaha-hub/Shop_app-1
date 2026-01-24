from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.auth.schemas import UserRegister, UserRead, ChengePasswordSchemas, Token
from app.auth.repository import UserRepository
from app.auth.exceptions import InvalidUsernamePassword, UsernameAlreadyExist, EmailAlreadyExist, InvalidToken
from app.auth.servises import PasswordServises, TokenServises


class AuthManager:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session
        self.user_repository = UserRepository(session)
        self.password_service = PasswordServises()
        self.token_service = TokenServises()

    async def login(
            self,
            username: str,
            password: str,

    ) -> Token:
        """
        Метод для входа в учёт запись

        проверяет наличие username в БД
        проверяет правильность пароль с БД

        :param username: имя пользователя
        :param password: пароль

        :return: Unauthorized: Ошибка авторизации

        :return: JWT token
        """
        user = await self.user_repository.get_user_by_username(username)
        if not user:
            raise InvalidUsernamePassword(
                "Invalid username or password",
            )
        if self.password_service.verify(password, user.hashed_password):
            raise InvalidUsernamePassword(
                "Invalid username or password",
            )
        access_token = self.token_service.encode(str(user.id))
        refresh_token = self.token_service.encode(str(user.id), is_refresh=True)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def register(
            self,
            request: UserRegister
    ) -> User:
        """
        Метод для регистрации пользователя

        проверят наличие username в БД

        проверяет наличие почты

        Хэширует пароль

        Создаёт пользователя в БД


        :param request: объект модельки
        :return: Моделька созданного пользователя
        """

        user = await self.user_repository.get_user_by_username(request.username)
        if user:
            raise UsernameAlreadyExist(
                "Username already exist",
            )
        user = await self.user_repository.get_user_by_email(request.email)
        if user:
            raise EmailAlreadyExist(
                "Email already exist",
            )

        hashed_password = self.password_service.hash(request.password)

        user = await self.user_repository.create_user(
            username=request.username,
            email=request.email,
            hashed_password=hashed_password,
            full_name=request.full_name,
        )
        await self.session.commit()
        return user

    async def get_me(
            self,
            token: str,
    ) -> User:
        """
        Метод для получения информации о пользователе

        Проверяем токен на валидность

        Берём информацию по ИД из БД

        :param token: JWT token
        :return: Моделька пользователя
        """
        payload = self.token_service.decode(token)

        if payload.get("is_expired", True):
            raise InvalidToken(
                "Invalid token",
            )

        if not payload.get("sub") or not payload.get("sub").isdigit():
            raise InvalidToken(
                "Invalid token",
            )

        user = await self.user_repository.get_user_by_id(int(payload.get("sub")))

        if not user:
            raise InvalidToken(
                "Invalid token",
            )
        return user

    async def change_password(
            self,
            user: User,
            request: ChengePasswordSchemas,

    ) -> None:
        """
        Метод изменение пароля

        Проверка наличия пользователя

        проверяет старый пароль пользователя и хэширует новый пароль

        Изменяет пароль в БД



        :param user: Пользователь
        :param request: Моделька
        :return: ничего
        """

        if self.password_service.verify(request.old_password, user.hashed_password):
            raise InvalidUsernamePassword(
                "Invalid username or password",
            )

        hashed_password = self.password_service.hash(request.new_password)

        await self.user_repository.update_password(
            user.id,
            hashed_password,
        )
        await self.session.commit()

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
        payload = self.token_service.decode(token)

        if not payload.get("is_refresh"):
            raise InvalidToken(
                "Invalid token",
            )

        if not payload.get("sub") or not payload.get("sub").isdigit():
            raise InvalidToken(
                "Invalid token",
            )

        access_token = self.token_service.encode(payload.get("sub"))
        refresh_token = self.token_service.encode(payload.get("sub"), is_refresh=True)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )
