from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.manager import AuthManager
from app.auth.schemas import RoleEnum
from app.core.dependencies import get_db
from app.core.exceptions import Forbidden

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

from app.auth.models import User


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db)
) -> User:
    """
    Функция для возврата текущего пользователя

    :param token: токен из Headers(Authorization)
    :param session: асинхронная сессия из зависимости get_db
    :return: моделька пользователя
    """

    manager = AuthManager(session)
    user = await manager.get_me(token)
    return user

async def get_auth_manager(
    session: AsyncSession = Depends(get_db)
):
    """
    Функция для создания объекта AuthManager

    :param session: сессия дб
    :return: объект AuthManager
    """
    return AuthManager(session)


async def is_admin(
        user: User = Depends(get_current_user)
):
    """
    Функция для проверки является ли пользователь админом

    :param user: моделька пользователя

    :return: моделька пользователя
    """
    if user.role != RoleEnum.admin.value:
        raise Forbidden(
            "You don't have access"
        )
    return user