from fastapi_filter.contrib.sqlalchemy import Filter

from app.product.models import Product


class ProductFilter(Filter):
    q: str = None

    category_id: int = None

    order_by: list[str] = None

    class Constants(Filter.Constants):
        model = Product
        search_model_fields = ("name",)
        search_field_name = "q"
