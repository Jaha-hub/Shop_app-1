

from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    """
    Базовая Pydantic моделька категории

    Attributes:
        name: название категории
        description: описание категории
    """
    name: str = Field(max_length=512)
    description: str = Field(max_length=1024)


class CategoryCreate(CategoryBase):
    """
    Pydantic моделька для создания категории

    Attributes:
        name: название категории
        description: описание категории
    """
    pass


class CategoryUpdate(CategoryBase):
    """
    Pydantic моделька для обновления категории

    Attributes:
        name: название категории
        description: описание категории
        """
    pass


class CategoryRead(CategoryBase):
    """
    Pydantic моделька для просмотра категории

    Attributes:
        id: ИД категории
        name: название категории
        description: описание категории
    """
    id: int