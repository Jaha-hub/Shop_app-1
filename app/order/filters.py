from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter

from app.order.models import Order
from app.order.schemas import OrderStatusEnum


class OrderFilter(Filter):
    id: Optional[int] = None
    status: Optional[OrderStatusEnum] = None

    class Constants(Filter.Constants):
        model = Order