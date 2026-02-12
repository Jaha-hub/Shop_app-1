from app.product.routers.product import router as product_router
from app.product.routers.characteristics import router as characteristics_router

product_router.include_router(characteristics_router)