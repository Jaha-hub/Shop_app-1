from sqlalchemy.ext.asyncio import AsyncSession

from app.category.dependencies import get_category_or_404
from app.product.exceptions import ProductNotFound
from app.product.models import Product
from app.product.repositories.product_repo import ProductRepository
from app.product.schemas import ProductCreate, ProductUpdate


class ProductManager:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session
        self.product_repo = ProductRepository(session)


    async def create_product(
            self,
            request: ProductCreate
    ) -> Product:
        """
        Метод для создания продукта

        :param request: запрос с данными для создания

        :return: созданный продукт
        """
        await get_category_or_404(request.category_id, self.session)
        product = await self.product_repo.create(
            **request.model_dump()
        )
        await self.session.commit()
        return product


    async def get_product(
            self,
            product_id: int
    ) -> Product:
        """
        Метод для получения продукта по ИД

        :param product_id: ИД продукта

        :return: моделька продукт
        """
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise ProductNotFound(
                "Продукт не найден"
            )
        return product


    # TODO
    async def get_all(self):
        pass


    async def update_product(
            self,
            request: ProductUpdate,
            product: Product
    ) -> None:
        """
        Метод для обновления продукта

        :param request: запрос с данными для обновления
        :param product: моделька продукта

        :return: ничего
        """
        if request.category_id != product.category_id:
            await get_category_or_404(request.category_id, self.session)

        await self.product_repo.update(
            product,
            **request.model_dump()
        )
        await self.session.commit()



    async def delete_product(
            self,
            product: Product
    ) -> None:
        """
        Метод для удаления продукта

        :param product: моделька продукта

        :return: ничего
        """

        await self.product_repo.delete(
            product
        )
        await self.session.commit()
