from app.auth.models import User
from app.core.exceptions import NotFound
from app.order.filters import OrderFilter
from app.order.models import Order
from app.order.repositories.order import OrderRepository
from app.order.repositories.order_product import OrderProductRepository
from app.order.schemas import OrderCreate


class OrderManager:
    def __init__(self, session):
        self.session = session
        self.repo = OrderRepository(session)
        self.order_product_repo = OrderProductRepository(session)

    async def create(
            self,
            request: OrderCreate,
            user: User
    ):
        order = await self.repo.create(
            user_id=user.id,
            **request.model_dump(exclude={"products"})
        )
        await self.order_product_repo.create(
            request.products,
            order=order
        )

        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def get_by_id(
            self,
            order_id: int
    ) -> Order:
        order = await self.repo.get_by_id(order_id)
        if not order:
            raise NotFound("Order not found")
        return order

    async def delete(
            self,
            order: Order
    ):
        await self.repo.delete(order)

    async def list(
            self,
            filters: OrderFilter
    ):
        orders = await self.repo.get_all(filters=filters)
        return orders


