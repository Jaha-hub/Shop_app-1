from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.order.models import OrderProducts


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            order_id,
            product_id,
            quantity,
            price,
    ) -> OrderProducts:
        stmt = insert(OrderProducts).values(
            order_id=order_id,
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

            order_id,
            product_id,
            quantity,
            price,
            

    ) -> None:
        order.user_id = user_id
        order.address = address
        order.comment = comment
        order.status = status
        order.phone = phone
        self.session.add(order)
        await self.session.flush()

    async def delete(
            self,
            order: Order,
    ) -> None:
        await self.session.delete(order)
        await self.session.flush()

    async def get_by_id(
            self,
            order_id: int
    ) -> Order:
        stmt = select(Order).where(Order.id == order_id)
        result = await self.session.execute(stmt)
        product = result.scalar_one_or_none()
        return product

    async def get_all(self):
        stmt = select(Order)
        result = await self.session.execute(stmt)
        order = result.scalars().all()
        return order
