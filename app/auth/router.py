from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from starlette import status

from app.auth.dependencies import get_auth_manager, get_current_user, oauth2_scheme
from app.auth.manager import AuthManager
from app.auth.models import User
from app.auth.schemas import Token, UserRead, UserRegister, ChangePasswordSchema, RefreshToken

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# OAuth2PasswordRequestForm - multipart-data


@cbv(router)
class AuthRouter:
    manager: AuthManager = Depends(get_auth_manager)

    @router.post(
        "/login", # путь
        summary="авторизация в систему", # название
        response_model=Token, # что вернет
        status_code=status.HTTP_200_OK, # успешный статус код
        responses = {

        } # какие еще ответы он может вернуть
    )
    async def login(
            self,
            form_data: OAuth2PasswordRequestForm = Depends(),
    ):
        """
        Эндпоинт для входа в учетную запись
        """
        response = await self.manager.login(form_data.username, form_data.password)
        return response


    @router.post(
        "/register",
        summary="регистрация пользователя",
        response_model=UserRead,
        status_code=status.HTTP_200_OK,
        responses={

        }
    )
    async def register(
            self,
            request: UserRegister,
    ):
        """
        Эндпоинт для регистрации
        """
        response = await self.manager.register(request)
        return response



    @router.get(
        "/me",
        summary="получение текущего пользователя",
        response_model=UserRead,
        status_code=status.HTTP_200_OK,
        responses={

        }
    )
    async def get_me(
            self,
            user: User = Depends(get_current_user),
    ):
        """
        Эндпоинт для получения текущего пользователя
        """
        return user
    


    @router.post(
        "/change_password",
        summary="изменение пароля",
        status_code=status.HTTP_200_OK,
        responses={

        }
    )
    async def change_password(
            self,
            request: ChangePasswordSchema,
            user: User = Depends(get_current_user),
    ):
        """
        Эндпоинт для изменения пароля пользователя
        """
        response = await self.manager.change_password(user, request)
        return response


    @router.post(
        "/refresh",
        summary="обновление токена",
        status_code=status.HTTP_200_OK,
        responses={

        }
    )
    async def refresh(
            self,
            request: RefreshToken,
    ):
        """
        Эндпоинт для обновления токена
        """
        response = await self.manager.refresh_token(request.refresh_token)
        return response