from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette import status

from app.auth.dependencies import is_admin
from app.category.dependencies import get_category_manager
from app.category.manager import CategoryManager
from app.category.schemas import CategoryCreate, CategoryUpdate

router = APIRouter(
    prefix="/categories",
    tags=["category"]
)


@cbv(router)
class AuthRouter:
    manager: CategoryManager = Depends(get_category_manager)

    @router.post(
        "/",
        summary="создание категории",
        status_code=status.HTTP_200_OK,
        dependencies=[
            Depends(is_admin)
        ]
    )
    async def create(
            self,
            request: CategoryCreate,
    ):
        """
        Эндпоинт для создания категории
        """
        response = await self.manager.create_category(request)
        return response


    @router.get(
        "/{category_id}",
        summary="получение категории по ид",
        status_code=status.HTTP_200_OK,
    )
    async def get_by_id(
            self,
            category_id: int,
    ):
        """
        Эндпоинт для получения категории по ид
        """
        response = await self.manager.get_category(category_id)
        return response


    @router.get(
        "/",
        summary="получение категорий",
        status_code=status.HTTP_200_OK,
    )
    async def get_all(
            self,
    ):
        """
        Эндпоинт для получения всех категорий
        """
        response = await self.manager.get_all_categories()
        return response


    @router.put(
        "/",
        summary="обновление категории",
        status_code=status.HTTP_200_OK,
        dependencies=[
            Depends(is_admin)
        ]
    )
    async def update(
            self,
            category_id: int,
            request: CategoryUpdate
    ):
        """
        Эндпоинт для обновления категории
        """
        response = await self.manager.update_category(category_id, request)
        return response


    @router.delete(
        "/",
        summary="удаление категории",
        status_code=status.HTTP_200_OK,
        dependencies=[
            Depends(is_admin)
        ]
    )
    async def delete(
            self,
            category_id: int
    ):
        """
        Эндпоинт для удаления категории
        """
        response = await self.manager.delete_category(category_id)
        return response