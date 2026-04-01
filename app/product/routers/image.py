from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse
from fastapi_utils.cbv import cbv

from app.product.dependencies import get_product_or_404, get_product_image_manager, get_product_image_or_404
from app.product.managers.image_manager import ProductImageManager
from app.product.models import Product, ProductImages

router = APIRouter(
    prefix="/{product_id}/images",
    tags=["images","products"],
)

@cbv(router)
class ImageRouter:
    manager: ProductImageManager = Depends(get_product_image_manager)
    product: Product = Depends(get_product_or_404)
    @router.post("/")
    async def upload(
            self,
            file: UploadFile = File(...)
    ):
        await self.manager.create(
            product=self.product,
            file=file,
        )

    async def delete(
            self,
            image: ProductImages = Depends(get_product_image_or_404)
    ):
        await self.manager.delete(
            image=image
        )

    async def get_image(
            self,
            image: ProductImages = Depends(get_product_image_or_404)
    ):
        return FileResponse(image.file_path)