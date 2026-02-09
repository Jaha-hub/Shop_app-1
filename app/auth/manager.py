
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.exceptions import InvalidUsernamePassword, UsernameAlreadyExist, EmailAlreadyExist, InvalidToken
from app.auth.models import User
from app.auth.repository import UserRepository
from app.auth.schemas import UserRegister, UserRead, ChangePasswordSchema, Token
from app.auth.services import PasswordService, TokenService


class AuthManager:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session
        self.user_repo = UserRepository(session)
        self.password_service = PasswordService()
        self.token_service = TokenService()


    async def login(
            self,
            username: str,
            password: str,
    ) -> Token:
        """
        Метод для входа в учетную запись

        Проверяет наличие указанного юзернейма в бд

        Проверяет правильность указанного пароля

        :param username: имя пользователя
        :param password: пароль

        :raise Unauthorized: Ошибка авторизации

        :return: JWT токен
        """

        user = await self.user_repo.get_user_by_username(username)
        if not user:
            raise InvalidUsernamePassword(
                "Invalid username or password",
            )

        if not self.password_service.verify(password, user.hashed_password):
            raise InvalidUsernamePassword("Invalid username or password")

        access_token = self.token_service.encode(str(user.id))
        refresh_token = self.token_service.encode(str(user.id), True)

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

        Проверяет наличие юзернейма в бд

        Проверяет наличие почты в бд

        Хэширует пароль

        Создает пользователя в бд


        :param request: объект Pydantic модельки


        :return: моделька созданного пользователя
        """

        user = await self.user_repo.get_user_by_username(request.username)
        if user:
            raise UsernameAlreadyExist(
                "Username already exist",
            )

        user = await self.user_repo.get_user_by_email(request.email)
        if user:
            raise EmailAlreadyExist(
                "Email already exist",
            )

        hashed_password = self.password_service.hash(request.password)

        # user = await self.user_repo.create(
        #     username=request.username,
        #     email=request.email,
        #     hashed_password=hashed_password,
        #     fullname=request.fullname,
        # )
        #
        user = await self.user_repo.create(
            hashed_password=hashed_password,
            **request.model_dump(
                exclude={"password"},
            )
        )
        await self.session.commit()
        return user


    async def get_me(
            self,
            token: str
    ) -> User:
        """
        Метод для получения информации пользователя

        Проверяет токен на валидность

        Достает информацию по ИД из бд

        :param token: JWT токен
        :return:  моделька токена
        """

        payload = self.token_service.decode(token)
        if payload.get("is_refresh", True):
            raise InvalidToken(
                "Invalid credentials",
            )

        if not payload.get("sub") or not payload.get("sub").isdigit():
            raise InvalidToken(
                "Invalid credentials",
            )

        user = await self.user_repo.get_user_by_id(int(payload.get("sub")))
        if not user:
            raise InvalidToken(
                "Invalid credentials"
            )
        return user


    async def change_password(
            self,
            user: User,
            request: ChangePasswordSchema
    ) -> None:
        """
        Метод изменения пароля

        Проверяет старый пароль пользователя

        Хэширует новый пароль

        Изменяет пароль в бд

        :param user: моделька пользователя
        :param request: объект Pydantic модельки
        :return: ничего
        """

        if not self.password_service.verify(request.old_password, user.hashed_password):
            raise InvalidUsernamePassword("Invalid username or password")

        hashed_password = self.password_service.hash(request.new_password)

        await self.user_repo.update_password(
            user.id,
            hashed_password,
        )

        await self.session.commit()


    async def refresh_token(
            self,
            token: str
    ):
        """
        Метод для обновления токена

        Проверяет валидность токена

        Создает новую пару токенов

        :param token: JWT токен

        :return: JWT токен
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
        refresh_token = self.token_service.encode(payload.get("sub"), True)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )