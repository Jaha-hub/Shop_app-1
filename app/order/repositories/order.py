from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.order.models import Order


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            user_id,
            address,
            comment,
            status,
            phone,
    ) -> Order:
        stmt = insert(Order).values(
            user_id=user_id,
            address=address,
            comment=comment,
            status=status,
            phone=phone,
        ).returning(Order)

        result = await self.session.execute(stmt)
        await self.session.flush()
        product = result.scalars().first()
        return product

    async def update(
            self,
            order: Order,
            address,
            comment,
            status,
            phone,
    ) -> None:
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
        order = result.scalar_one_or_none()
        return order

    async def get_all(
            self,
            filters
    ):
        stmt = select(Order)
        if filters:
            stmt = filters.filter(stmt)
            stmt = filters.sort(stmt)
        result = await self.session.execute(stmt)
        order = result.scalars().all()
        return order
