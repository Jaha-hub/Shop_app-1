from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_utils.cbv import cbv

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.order.dependencies import get_order_manager, get_order_or_404
from app.order.filters import OrderFilter
from app.order.managers.order import OrderManager
from app.order.models import Order
from app.order.schemas import OrderCreate, OrderUpdate

router = APIRouter(
    prefix="/order",
    tags=["order"]
)


@cbv(router)
class OrderRouter:
    manager: OrderManager = Depends(get_order_manager)

    @router.get("/")
    async def list(
            self,
            filters: OrderFilter = FilterDepends(OrderFilter),
    ):
        return await self.manager.list(filters)

    @router.get("/{order_id}")
    async def get_by_id(
            self,
            order_id: int,
    ):
        order = await self.manager.get_by_id(
            order_id=order_id
        )
        return order

    @router.post("/")
    async def create(
            self,
            request: OrderCreate,
            user: User = Depends(get_current_user),
    ):
        order = await self.manager.create(
            request=request,
            user=user,
        )
        return order

    @router.delete("/{order_id}")
    async def delete(
            self,
            order: Order = Depends(get_order_or_404),
    ):
        await self.manager.delete(order)

    @router.put("/{order_id}")
    async def update(
            self,
            request: OrderUpdate,
            order: Order = Depends(get_order_or_404),
    ):
        await self.manager.update(request,order)
