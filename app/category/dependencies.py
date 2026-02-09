from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.category.manager import CategoryManager
from app.core.dependencies import get_db


async def get_category_manager(
    session: AsyncSession = Depends(get_db)
):
    """
    Функция для создания объекта CategoryManager
    :param session: сессия бд
    :return: объект CategoryManager
    """
    return CategoryManager(session)


async def get_category_or_404(
    category_id: int,
    session: AsyncSession = Depends(get_db)
):
    """
    Функция для поиска категории
    Если категории нет вызывает ошибку 404

    :param category_id: ИД категории
    :param session: сессия бд

    :return: моделька категории
    """

    manager = CategoryManager(session)
    return await manager.get_category(category_id)