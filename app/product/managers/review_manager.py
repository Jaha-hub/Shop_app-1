from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User

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
            user: User,
            product: Product,
    ) -> ProductReview:
        product = await self.review_repo.create(
            **request.model_dump(),
            user_id=user.id,
            product_id=product.id,
        )
        await self.session.commit()
        return product

    async def get_review(
            self,
            product: Product,
            review_id: int
    ) -> ProductReview:

        product = await self.review_repo.get_by_id(review_id, product.id)
        if not product:
            raise ReviewNotFound(
                "Продукт не найден"
            )
        return product

    async def get_all(self) -> list[ProductReview]:
        reviews = await self.review_repo.get_all()
        return reviews

    async def update_review(
            self,
            request: ProductReviewUpdate,
            product: ProductReview
    ) -> None:
        """
        Метод для обновления продукта

        :param request: запрос с данными для обновления
        :param product: моделька продукта

        :return: ничего
        """


        await self.review_repo.update(
            product,
            **request.model_dump()
        )
        await self.session.commit()

    async def delete_review(
            self,
            product: ProductReview
    ) -> None:
        """
        Метод для удаления продукта

        :param product: моделька продукта

        :return: ничего
        """

        await self.review_repo.delete(
            product
        )
        await self.session.commit()
