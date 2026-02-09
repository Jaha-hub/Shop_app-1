from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.product.models import Product


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            name,
            short_description,
            long_description,
            price,
            category_id
    ) -> Product:
        """
        Функция для создания продукта

        :param name: название продукта
        :param short_description: краткое описание продукта
        :param long_description: длинное описание продукта
        :param price: цена продукта
        :param category_id: Ид категории продукта


        :return: моделька продукта
        """

        stmt = insert(Product).values(
            name=name,
            short_description=short_description,
            long_description=long_description,
            price=price,
            category_id=category_id
        ).returning(Product)

        result = await self.session.execute(stmt)
        await self.session.flush()
        product = result.scalars().first()
        return product


    async def update(
            self,
            product: Product,
            name,
            short_description,
            long_description,
            price,
            category_id
    ) -> None:
        """
        Функция для обновления продукта

        :param product: моделька продукта
        :param name: название продукта
        :param short_description: краткое описание продукта
        :param long_description: длинное описание продукта
        :param price: цена продукта
        :param category_id: Ид категории продукта


        :return: ничего
        """

        product.name = name
        product.short_description = short_description
        product.long_description = long_description
        product.price = price
        product.category_id = category_id
        self.session.add(product)
        await self.session.flush()


    async def delete(
            self,
            product: Product,
    ) -> None:
        """
        Функция для удаления продукта

        :param product: моделька продукта

        :return: ничего
        """

        await self.session.delete(product)
        await self.session.flush()


    async def get_by_id(
            self,
            product_id: int
    ) -> Product:
        """
        Функция для получения продукта по ИД

        :param product_id: Ид продукта

        :return: моделька продукта
        """

        stmt = select(Product).where(Product.id == product_id)
        result = await self.session.execute(stmt)
        product = result.scalar_one_or_none()
        return product


    async def get_all(self):
        pass
