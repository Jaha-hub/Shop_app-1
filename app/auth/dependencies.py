from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.manager import AuthManager
from app.core.dependencies import get_db

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession=Depends(get_db)
):
    """
    Функция для возврата текущего пользователя


    :param token: Токен
    :param session: Сессия
    :return: Модель Пользователя
    """


    manager = AuthManager(session)
    user = await manager.get_me(token=token)
    return user


async def get_auth_manager(
        session: AsyncSession=Depends(get_db),

):
    """
    Функция для создания объекта AuthManager


    :param session: сессия
    :return: объект AuthManager
    """
    return AuthManager(session)