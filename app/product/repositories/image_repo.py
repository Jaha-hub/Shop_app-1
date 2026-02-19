from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.product.models import ProductImages


class ProductImageRepository:
    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session

    async def create(
            self,
            product_id: int,
            filename,
            file_path,
    ):
        image = ProductImages(
            product_id=product_id,
            filename=filename,
        )
        self.session.add(image)
        await self.session.flush()

    async def delete(
            self,
            image: ProductImages
    )-> None:
        await self.session.delete(image)
        await self.session.flush()

    async def get_by_id(
            self,
            filename: str,
    ):
        stmt = select(ProductImages).where(ProductImages.filename == filename)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()