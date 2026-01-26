from sqlalchemy import Select, Insert, Update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.category.models import Categories


class CategoryRepository:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session

    async def create_category(
            self,
            name: str,
            description: str,
    ) -> Categories:
        stmt = Insert(Categories).values(
            name=name,
            description=description,
        ).returning(Categories)
        result = await self.session.execute(stmt)
        await self.session.flush()
        category = result.scalars().first()
        return category

    async def update_category(
            self,
            category_id: int,
            name: str,
            description: str,
    ) -> None:
        stmt = Update(Categories).where(Categories.id == category_id).values(
            name=name,
            description=description,
        )
        await self.session.execute(stmt)
        await self.session.flush()


    async def delete_category(
            self,
            category_id: int,
    ) -> None:
        stmt = delete(Categories).where(Categories.id == category_id)
        await self.session.execute(stmt)


    async def get_categories(
            self,
    ) -> list:
        stmt= Select(Categories)
        categories = await self.session.execute(stmt)
        return categories.scalars().all()


    async def get_category_by_id(
            self,
            category_id: int,
    ):
        stmt = Select(Categories).where(Categories.id == category_id)
        category = await self.session.execute(stmt)
        return category.scalar_one_or_none()