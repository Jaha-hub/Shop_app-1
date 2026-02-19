from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.core.dependencies import get_db
from app.core.exceptions import Forbidden, NotFound
from app.product.managers.characteristics_manager import ProductCharacteristicsManager
from app.product.managers.image_manager import ProductImageManager
from app.product.managers.product_manager import ProductManager
from app.product.managers.review_manager import ProductReviewManager
from app.product.models import Product, ProductReview


async def get_product_manager(
        session: AsyncSession = Depends(get_db)
):
    return ProductManager(session)


async def get_product_or_404(
        product_id: int,
        manager: ProductManager = Depends(get_product_manager),
):
    return await manager.get_product(product_id)



async def get_characteristics_manager(
        session: AsyncSession = Depends(get_db)
):
    return ProductCharacteristicsManager(session)



async def get_characteristics_or_404(
        characteristic_id: int,
        product: Product = Depends(get_product_or_404),
        manager: ProductCharacteristicsManager = Depends(get_product_manager),
):
    return await manager.get_characteristic(characteristic_id=characteristic_id, product=product)


async def get_review_or_404(
        review_id: int,
        product: Product = Depends(get_product_or_404),
        session: AsyncSession = Depends(get_db)
):
    manager = ProductReviewManager(session)
    return await manager.get_review(review_id= review_id,product=product)

async def get_review_manager(
    session: AsyncSession = Depends(get_db)
):
    return ProductReviewManager(session)



async def is_review_owner(
        review: ProductReview  = Depends(get_review_or_404),
        user: User = Depends(get_current_user)
) -> None:

    if user.id != review.user_id:
        raise Forbidden(
            "You don't have permission"
        )




async def get_product_image_manager(
        session: AsyncSession = Depends(get_db)
):
    return ProductImageManager(session)

async def get_product_image_or_404(
        file_name: str,
        product: Product = Depends(get_product_or_404),
        manager: ProductImageManager = Depends(get_product_image_manager),
):
    image = await manager.get(file_name)
    if not image.product_id != product.id:
        raise NotFound(
            f"Product {product.id} doesn't exist"
        )
    return image