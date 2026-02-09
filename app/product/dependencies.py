from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.core.dependencies import get_db
from app.core.exceptions import Forbidden
from app.product.managers.characteristics_manager import ProductCharacteristicsManager
from app.product.managers.product_manager import ProductManager
from app.product.managers.review_manager import ProductReviewManager
from app.product.models import ProductReview


async def get_product_or_404(
    product_id: int,
    session: AsyncSession = Depends(get_db)
):
    """
    Функция для поиска продукта
    Если продукта нет вызывает ошибку 404

    :param product_id: ИД продукта
    :param session: сессия бд

    :return: моделька продукта
    """

    manager = ProductManager(session)
    return await manager.get_product(product_id)


async def get_characteristics_or_404(
    characteristic_id: int,
    session: AsyncSession = Depends(get_db)
):
    """
    Функция для поиска характеристики продукта
    Если характеристики нет вызывает ошибку 404

    :param characteristic_id: ИД характеристики
    :param session: сессия бд

    :return: моделька характеристики
    """

    manager = ProductCharacteristicsManager(session)
    return await manager.get_characteristic(characteristic_id)


async def get_review_or_404(
    review_id: int,
    session: AsyncSession = Depends(get_db)
):
    """
    Функция для поиска отзыва
    Если отзыва нет вызывает ошибку 404

    :param review_id: ИД отзыва
    :param session: сессия бд

    :return: моделька отзыва
    """

    manager = ProductReviewManager(session)
    return await manager.get_review(review_id)


async def is_review_owner(
        review: ProductReview,
        user: User = Depends(get_current_user)
) -> None:
    """
    Функция для проверки является ли пользователь автором отзыва

    :param review: моделька отзыва
    :param user: моделька пользователя

    :return: ничего
    """
    if user.id != review.user_id:
        raise Forbidden(
            "You don't have permission"
        )



