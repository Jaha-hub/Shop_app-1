from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from fastapi_filter import FilterDepends
from fastapi_utils.cbv import cbv
from sqlalchemy.util import await_only

from app.product.dependencies import get_product_manager
from app.product.filters import ProductFilter
from app.product.managers.product_manager import ProductManager
from app.product.models import Product
from app.product.schemas import ProductCreate, ProductUpdate

router = APIRouter(
    prefix="/product",
    tags=["product"],
)


@cbv
class ProductRouter:
    manager: ProductManager = Depends(get_product_manager)

    @router.get("/")
    async def list(
            self,
            filters: ProductFilter = FilterDepends(ProductFilter),

    ):
        return await self.manager.get_all(filters)

    @router.get("/{id}")
    async def get_product(
            self,
            product: Product = Depends(get_product_manager),
    ):
        return product

    @router.post("/")
    async def create_product(
            self,
            request: ProductCreate,
    ):
        await self.manager.create_product(request)

    @router.put("/{id}")
    async def update_product(
            self,
            request: ProductUpdate,
            product: Product = Depends(get_product_manager),
    ):
        await self.manager.update_product(request=request, product=product)

    @router.delete("/{id}")
    async def delete_product(
            self,
            product: Product = Depends(get_product_manager),
    ):
        await self.manager.delete_product(product=product)
