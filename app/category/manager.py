from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.category.models import Categories
from app.category.schemas import CategoryCreate, CategoryUpdate, CategoryDelete, CategoryRead
from app.category.repository import CategoryRepository
from app.core.dependencies import get_db


class CategoryManager:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session = Depends(get_db)
        self.category_repository = CategoryRepository(session)

    async def create_category(
            self,
            request: CategoryCreate,
    ) -> Categories:
        category = await self.category_repository.create_category(
            name=request.name,
            description=request.description,
        )
        await self.session.commit()
        return category

    async def update_category(
            self,
            request: CategoryUpdate,
    ) -> None:
        category = await self.category_repository.update_category(
            category_id=request.category_id,
            name=request.name,
            description=request.description,
        )
        await self.session.commit()
        return category

    async def delete_category(
            self,
            request: CategoryDelete,
    ) -> None:
        await self.category_repository.delete_category(
            category_id=request.category_id,
        )

    async def read_category(
            self,
            request: CategoryRead,
    ) -> Categories:
        category = await self.category_repository.get_category_by_id(
            category_id=request.category_id,
        )
        return category

    async def get_all_categories(
            self,
    ) -> list:
        category = await self.category_repository.get_categories()
        return category
