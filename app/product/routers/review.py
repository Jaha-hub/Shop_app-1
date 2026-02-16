from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.product.dependencies import get_review_manager, get_product_or_404, get_review_or_404, is_review_owner
from app.product.managers.review_manager import ProductReviewManager
from app.product.models import Product, ProductReview
from app.product.schemas import ProductReviewCreate, ProductReviewUpdate

router = APIRouter(
    prefix="/{product_id}/review",
    tags=["reviews"]
)


@cbv(router)
class ReviewRouter:
    manager: ProductReviewManager = Depends(get_review_manager)

    @router.post("/")
    async def create(
            self,
            request: ProductReviewCreate,
            product: Product = Depends(get_product_or_404),
            user: User = Depends(get_current_user),
    ):
        await self.manager.create_review(request, user, product)

    @router.get("/")
    async def list(
            self,
            product: Product = Depends(get_product_or_404),
    ):
        reviews = await self.manager.get_all(product)
        return reviews

    @router.get("/{review_id}")
    async def detail(
            self,
            reviews: ProductReview = Depends(get_review_or_404)
    ):
        return reviews

    @router.put(
        "/{review_id}",
        dependencies=[
            Depends(is_review_owner)
        ]
    )
    async def update(
            self,
            request: ProductReviewUpdate,
            review: ProductReview = Depends(get_review_or_404),
    ):
        await self.manager.update_review(request, review)

    @router.delete(
        "/{review_id}",
        dependencies=[
            Depends(is_review_owner)
        ]
    )
    async def delete(
            self,
            reviews: ProductReview = Depends(get_review_or_404),
    ):
        await self.manager.delete_review(reviews)
