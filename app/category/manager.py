from sqlalchemy.ext.asyncio import AsyncSession

from app.category.exceptions import CategoryNotFound
from app.category.models import Category
from app.category.repository import CategoryRepository
from app.category.schemas import CategoryCreate, CategoryRead, CategoryUpdate


class CategoryManager:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session
        self.category_repo = CategoryRepository(session)


    async def create_category(
            self,
            request: CategoryCreate,
    ) -> Category:
        """
        Метод для создания категории

        :param request: запрос с данными для создания

        :return: созданная категория
        """

        category = await self.category_repo.create_category(
            name=request.name,
            description=request.description,
        )
        await self.session.commit()
        return category


    async def get_category(
            self,
            category_id: int,
    ) -> Category:
        """
        Метод для получения категории по ИД

        :param category_id: ИД категории

        :return: категория
        """
        category = await self.category_repo.get_category_by_id(category_id)
        if not category:
            raise CategoryNotFound(
                "Category not found"
            )
        return category


    async def get_all_categories(
            self    ) -> list[Category]:
        """
        Метод для получения всех категорий

        :return: список категорий
        """
        categories = await self.category_repo.get_categories()
        return categories


    async def update_category(
            self,
            category_id: int,
            request: CategoryUpdate,
    ) -> None:
        """
        Метод для обновления категории

        :param category_id: ИД категории
        :param request: запрос с данными для обновления

        :return: ничего
        """
        await self.category_repo.update_category(
            category_id=category_id,
            name=request.name,
            description=request.description,
        )
        await self.session.commit()


    async def delete_category(
            self,
            category_id: int
    ) -> None:
        """
        Метод для удаления категории

        :param category_id: ИД категории

        :return: ничего
        """
        await self.category_repo.delete_category(
            category_id=category_id
        )
        await self.session.commit()


