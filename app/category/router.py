from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from fastapi_utils.cbv import cbv

from app.category.manager import CategoryManager
from app.category.schemas import CategoryRead, CategoryUpdate, CategoryCreate, CategoryDelete
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/category",
    tags=["category"],
)


@cbv(router)
class CategoriesRouter:
    session: AsyncSession = Depends(get_db)
    manager = CategoryManager(session=session)

    @router.post(
        "/register",
        summary="Регистрация в Систему",  # Название
        response_model=CategoryRead,  # что он вернёт
        status_code=status.HTTP_200_OK,  # Статус код
        responses={}

    )
    async def create_category(
            self,
            request: CategoryCreate
    ):
        response = await self.manager.create_category(
            request=request,
        )
        return response

    @router.post(
        "/update",
    )
    async def update_category(
            self,
            request: CategoryUpdate,
    ):
        await self.manager.update_category(
            request=request,
        )

        return {
            "category": "success",
        }

    @router.delete(
        "/delete",
    )
    async def delete_category(
            self,
            request: CategoryDelete,
    ):
        await self.manager.delete_category(
            request=request,
        )
        return {
            "category": "success",
        }

    @router.get(
        "/list",
    )
    async def get_categories(
            self,
    ):
        category = await self.manager.get_all_categories()
        return category

    @router.get(
        "/{category_id}",
    )
    async def get_category_by_id(
            self,
            request: CategoryRead,
    ):
        category = await self.manager.read_category(
            request=request
        )
        return category
