from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.order.managers.order import OrderManager
from app.order.models import OrderProducts


async def get_order_manager(
        session: AsyncSession = Depends(get_db)
):
    return OrderManager(session)

async def get_order_or_404(
        product_id: int,
        manager: OrderManager = Depends(get_order_manager),
):
    return await manager.get_by_id(product_id)


async def get_order_product_manager(
        session: AsyncSession = Depends(get_db)
):
    return OrderManager(session)

async def get_order_or_404(
        product_id: int,
        manager: OrderManager = Depends(get_order_manager),
):
    return await manager.get_by_id(product_id)