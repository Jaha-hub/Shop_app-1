from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from app.product.dependencies import get_characteristics_manager, get_characteristics_or_404, get_product_or_404
from app.product.managers.characteristics_manager import ProductCharacteristicsManager
from app.product.models import ProductCharacteristics, Product
from app.product.schemas import ProductCharacteristicsCreate, ProductCharacteristicsUpdate

router = APIRouter(
    prefix="/{product_id}/characteristics",
)


@cbv
class CharacteristicsRouter:
    manager: ProductCharacteristicsManager = Depends(get_characteristics_manager)

    @router.get("/")
    async def list(
            self,
            product: Product = Depends(get_product_or_404)
    ):
        return await self.manager.get_all(product=product)

    @router.get("/{characteristic_id}")
    async def get_characteristic(
            self,
            characteristic: ProductCharacteristics = Depends(get_characteristics_or_404),
    ):
        return characteristic

    @router.post("/")
    async def create_characteristic(
            self,
            request: ProductCharacteristicsCreate,
            product: Product = Depends(get_product_or_404),
    ):
        await self.manager.create_characteristic(product=product, request=request)

    @router.put("/{characteristic_id}")
    async def update_characteristic(
            self,
            request: ProductCharacteristicsUpdate,
            characteristic: ProductCharacteristics = Depends(get_characteristics_or_404),
    ):
        await self.manager.update_characteristic(characteristic=characteristic, request=request)

    @router.delete("/{characteristic_id}")
    async def delete_characteristic(
            self,
            characteristic: ProductCharacteristics = Depends(get_characteristics_or_404),
    ):
        await self.manager.delete_characteristic(characteristic=characteristic)
