from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.product.models import ProductCharacteristics


class ProductCharacteristicsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            name,
            value,
            product_id,
    ) -> ProductCharacteristics:
        """
        Функция для создания характеристики продукта

        :param name: название характеристики
        :param value: значение характеристики
        :param product_id: ИД продукта

        :return: моделька характеристики продукта
        """

        stmt = insert(ProductCharacteristics).values(
            name=name,
            value=value,
            product_id=product_id,
        ).returning(ProductCharacteristics)

        result = await self.session.execute(stmt)
        await self.session.flush()
        characteristics = result.scalars().first()
        return characteristics



    async def update(
            self,
            characteristic: ProductCharacteristics,
            name,
            value,
            product_id,
    ) -> None:
        """
        Функция для обновления характеристики продукта

        :param characteristic: моделька характеристики
        :param name: название характеристики
        :param value: значение характеристики
        :param product_id: ИД продукта

        :return: ничего
        """

        characteristic.name = name
        characteristic.value = value
        characteristic.product_id = product_id
        self.session.add(characteristic)
        await self.session.flush()



    async def delete(
            self,
            characteristic: ProductCharacteristics,
    ) -> None:
        """
        Функция для удаления характеристики продукта

        :param characteristic: моделька характеристики

        :return: ничего
        """

        await self.session.delete(characteristic)
        await self.session.flush()


    async def get_by_id(
            self,
            characteristic_id
    ) -> ProductCharacteristics:
        """
        Функция для получения характеристики продукта по ИД

        :param characteristic_id: Ид характеристики

        :return: моделька характеристики
        """

        stmt = select(ProductCharacteristics).where(ProductCharacteristics.id == characteristic_id)
        result = await self.session.execute(stmt)
        characteristics = result.scalar_one_or_none()
        return characteristics


    async def get_all(self):
        pass
