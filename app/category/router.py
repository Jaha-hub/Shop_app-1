from fastapi import Depends, APIRouter
from starlette import status


from fastapi_utils.cbv import cbv


from app.category.manager import CategoryManager
from app.category.schemas import CategoryRead, CategoryUpdate, CategoryCreate, CategoryDelete

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@cbv(router)
class CategoriesRouter:


    @router.post(
        "/register",
        summary="Регистрация в Систему",  # Название
        response_model=CategoryRead,  # что он вернёт
        status_code=status.HTTP_200_OK,  # Статус код
        responses={}

    )
    async def register(
            self,
            request: CategoryCreate
    ):
        response = await self.manager.register(
            request=request,
        )
        return response