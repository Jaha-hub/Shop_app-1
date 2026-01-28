from fastapi import Depends, APIRouter
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from fastapi_utils.cbv import cbv

from app.auth.dependencies import get_auth_manager
from app.auth.manager import AuthManager
from app.auth.schemas import Token, UserRead, UserRegister, ChengePasswordSchemas, RefreshToken

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


@cbv(router)
class AuthRouter:
    manager: AuthManager = Depends(get_auth_manager)

    # OAuth2PasswordRequestForm -> multipart-data

    @router.post(
        "/login",  # Путь
        summary="Авторизация в Систему",  # Название
        response_model=Token,  # что он вернёт
        status_code=status.HTTP_200_OK,  # Статус код
        responses={

        }
    )
    async def login(
            self,

            form_data: OAuth2PasswordRequestForm = Depends()
    ):
        """

        :param form_data:
        :return:
        """
        response = await self.manager.login(
            username=form_data.username,
            password=form_data.password,
        )
        return response

    @router.post(
        "/register",
        summary="Регистрация в Систему",  # Название
        response_model=UserRead,  # что он вернёт
        status_code=status.HTTP_200_OK,  # Статус код
        responses={}

    )
    async def register(
            self,
            request: UserRegister
    ):
        response = await self.manager.register(
            request=request,
        )
        return response

    @router.get(
        "/me",
        summary="Получить данные текущего пользователя",
        response_model=UserRead,
    )
    async def get_me(self, token: str = Depends(oauth2_scheme)):
        """
        🔹 Возвращает данные авторизованного пользователя.

        ### Требует:
        Bearer Token в заголовке Authorization.

        ### Логика:
        1. Декодирование JWT
        2. Проверка валидности
        3. Получение пользователя из БД

        ### Ошибки:
        - **401** — невалидный токен
        """
        user = await self.manager.get_me(token)
        return user

    @router.post(
        "/refresh",
        summary="Обновление пары токенов",
        response_model=Token,
    )
    async def refresh(self, token: RefreshToken):
        """
        🔹 Обновляет access и refresh токены.

        ### Требует:
        Refresh token в заголовке Authorization.

        ### Логика:
        1. Проверка, что токен refresh
        2. Генерация новой пары токенов

        ### Ошибки:
        - **401** — токен не refresh или невалидный
        """
        return await self.manager.refresh_token(token=token)

    @router.post(
        "/change-password",
        summary="Изменить пароль пользователя",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def change_password(
            self,
            request: ChengePasswordSchemas,
            token: str = Depends(oauth2_scheme),
    ):
        """
        🔹 Изменение пароля текущего пользователя.

        ### Параметры:
        - **old_password**
        - **new_password**

        ### Логика:
        1. Проверка токена
        2. Проверка старого пароля
        3. Хеширование нового
        4. Обновление в БД

        ### Ошибки:
        - **401** — неверный старый пароль
        """
        user = await self.manager.get_me(token)
        await self.manager.change_password(user, request)

