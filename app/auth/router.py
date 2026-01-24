from fastapi import Depends, APIRouter
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_utils.cbv import cbv

from app.auth.dependencies import get_auth_manager
from app.auth.manager import AuthManager
from app.auth.schemas import Token, UserRead, UserRegister

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@cbv(router)
class AuthRouter:
    manager: AuthManager = Depends(get_auth_manager),

    # OAuth2PasswordRequestForm -> multipart-data

    @router.post(
        "/login",  # Путь
        summary="Авторизация в Систему",  # Название
        response_model=Token,  # что он вернёт
        status_code=status.HTTP_200_OK,  # Статус код
        responses={

        }  # ещё статус коды
    )
    async def login(
            self,

            form_data: OAuth2PasswordRequestForm = Depends(),
    ):
        """

        :param form_data:
        :param manager:
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


