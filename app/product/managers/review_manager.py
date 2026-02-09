from sqlalchemy.ext.asyncio import AsyncSession

from app.product.dependencies import get_product_or_404
from app.product.exceptions import ReviewNotFound
from app.product.models import ProductReview, Product
from app.product.repositories.review_repo import ProductReviewRepository
from app.product.schemas import ProductReviewCreate, ProductReviewUpdate


class ProductReviewManager:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session
        self.review_repo = ProductReviewRepository(session)


    async def create_review(
            self,
            request: ProductReviewCreate,
            user_id: int,
            product_id: int
    ) -> ProductReview:
        """
        Метод для создания отзыва

        :param request: запрос с данными для создания
        :param user_id: ИД пользователя
        :param product_id: ИД продукта

        :return: созданный отзыв
        """

        await get_product_or_404(product_id, self.session)
        review = await self.review_repo.create(
            **request.model_dump(),
            user_id=user_id,
            product_id=product_id
        )
        await self.session.commit()
        return review


    async def get_review(
            self,
            review_id: int
    ) -> ProductReview:
        """
        Метод для получения отзыва по ИД

        :param review_id: ИД отзыва

        :return: моделька отзыва
        """
        review = await self.review_repo.get_by_id(review_id)
        if not review:
            raise ReviewNotFound(
                "Отзыв не найден"
            )
        return review


    # TODO
    async def get_all(self):
        pass


    async def update_review(
            self,
            request: ProductReviewUpdate,
            review: ProductReview,
            product: Product,
            user_id: int
    ) -> None:
        """
        Метод для обновления отзыва

        :param request: запрос с данными для обновления
        :param review: моделька отзыва
        :param product: моделька продукта
        :param user_id: ИД пользователя

        :return: ничего
        """

        await self.review_repo.update(
            review,
            **request.model_dump(),
            product_id=product.id,
            user_id=user_id,
        )
        await self.session.commit()



    async def delete_review(
            self,
            review: ProductReview
    ) -> None:
        """
        Метод для удаления отзыва

        :param review:: моделька отзыва

        :return: ничего
        """

        await self.review_repo.delete(
            review
        )
        await self.session.commit()
