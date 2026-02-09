from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.product.models import ProductReview


class ProductReviewRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            user_id,
            product_id,
            message,
            grade
    ) -> ProductReview:
        """
        Функция для создания отзыва продукта

        :param user_id: ИД пользователя
        :param product_id: ИД продукта
        :param message: текст
        :param grade: оценка

        :return: моделька отзыва
        """

        stmt = insert(ProductReview).values(
            user_id=user_id,
            product_id=product_id,
            message=message,
            grade=grade
        ).returning(ProductReview)

        result = await self.session.execute(stmt)
        await self.session.flush()
        review = result.scalars().first()
        return review


    async def update(
            self,
            review: ProductReview,
            user_id,
            product_id,
            message,
            grade
    ) -> None:
        """
        Функция для обновления отзыва продукта

        :param review: моделька отзыва
        :param user_id: ИД пользователя
        :param product_id: ИД продукта
        :param message: текст
        :param grade: оценка

        :return: ничего
        """

        review.user_id = user_id
        review.product_id = product_id
        review.message = message
        review.grade = grade
        self.session.add(review)
        await self.session.flush()


    async def delete(
            self,
            review: ProductReview
    ) -> None:
        """
        Функция для удаления отзыва продукта

        :param review: моделька отзыва

        :return: ничего
        """
        await self.session.delete(review)
        await self.session.flush()


    async def get_by_id(
            self,
            review_id
    ) -> ProductReview:
        """
        Функция для получения продукта по ИД

        :param review_id: Ид отзыва

        :return: моделька отзыва
        """

        stmt = select(ProductReview).where(ProductReview.id == review_id)
        result = await self.session.execute(stmt)
        review = result.scalar_one_or_none()
        return review


    async def get_all(self):
        pass
