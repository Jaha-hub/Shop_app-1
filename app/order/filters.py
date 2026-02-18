from fastapi_filter.contrib.sqlalchemy import Filter

from app.order.models import OrderProducts


class OrderFilter(Filter):
    q: str = None

    category_id: int = None

    order_by: list[str] = None

    class Constants(Filter.Constants):
        model = OrderProducts
        search_model_fields = ("status",)