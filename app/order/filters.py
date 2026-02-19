from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter

from app.order.models import Order
from app.order.schemas import OrderStatusEnum


class OrderFilter(Filter):
    q: str | None = None
    status: OrderStatusEnum | None = None
    user_id: int | None = None

    class Constants(Filter.Constants):
        model = Order
        search_model_fields = ["id"]
        search_field_name = "q"