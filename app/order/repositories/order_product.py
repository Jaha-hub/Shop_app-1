from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.order.models import OrderProducts, Order
from app.order.schemas import OrderProductCreate


class OrderProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            products: list[OrderProductCreate],
            order: Order
    ):
        order_products = [
            OrderProducts(
                order_id=order.id,
                quantity=product.quantity,
                product_id=product.product_id,
                price=product.price,
            )
            for product in products
        ]
        self.session.add_all(order_products)
        await self.session.flush()

    async def get_all(
            self,
            order_id: int
    ):
        stmt = select(OrderProducts).where(OrderProducts.order_id == order_id)
        result = await self.session.execute(stmt)
        products = result.scalars().all()
        return products

    async def get_by_id(
            self,
            order_id: int,
            product_id: int,
    ):
        stmt = select(OrderProducts).where(OrderProducts.order_id == order_id, OrderProducts.product_id == product_id)
        result = await self.session.execute(stmt)
        products = result.scalar_one_or_none()
        return products

    async def delete(
            self,
            order_product: OrderProducts
    ):
        await self.session.delete(order_product)
