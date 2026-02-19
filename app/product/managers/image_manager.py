import shutil
import uuid

from fastapi import UploadFile

from app.core.exceptions import NotFound
from app.core.settings import settings, BASE_DIR
from app.product.models import Product, ProductImages
from app.product.repositories.image_repo import ProductImageRepository
from app.product.repositories.product_repo import ProductRepository


class ProductImageManager:
    def __init__(
            self,
            session,
    ):
        self.session = session
        self.repo = ProductImageRepository(session)
        self.product_repo = ProductRepository(session)

    async def create(
            self,
            product: Product,
            file: UploadFile,
    ):
        filename = f"{uuid.uuid4()}-{file.filename}"
        file_path = BASE_DIR / "images" / filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        await self.repo.create(product.id, filename, file_path)
        await self.session.commit()

    async def delete(
            self,
            image: ProductImages
    ):
        await self.repo.delete(image)
        await self.session.commit()

    async def get(
            self,
            filename:str
    ):
        image = await self.repo.get_by_id(filename)
        if not image:
            raise NotFound("Image with filename {filename} not found")
        return image