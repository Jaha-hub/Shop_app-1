from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.order.models import OrderProducts


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            product_id,
            quantity,
            price,
    ) -> OrderProducts:
        stmt = insert(OrderProducts).values(
            product_id=product_id,
            quantity=quantity,
            price=price,
        ).returning(OrderProducts)

        result = await self.session.execute(stmt)
        await self.session.flush()
        product = result.scalars().first()
        return product

    async def update(
            self,
            order_product: OrderProducts,
            product_id,
            quantity,
            price,
            

    ) -> None:
        order_product.product_id = product_id
        order_product.quantity = quantity
        order_product.price = price
        self.session.add(order_product)
        await self.session.flush()

    async def delete(
            self,
            order: OrderProducts,
    ) -> None:
        await self.session.delete(order)
        await self.session.flush()

    async def get_by_id(
            self,
            order_id: int
    ) -> OrderProducts:
        stmt = select(OrderProducts).where(OrderProducts.id == order_id)
        result = await self.session.execute(stmt)
        product = result.scalar_one_or_none()
        return product

    async def get_all(self):
        stmt = select(OrderProducts)
        result = await self.session.execute(stmt)
        order = result.scalars().all()
        return order
