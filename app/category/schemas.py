from pydantic import  Field

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str = Field(min_length=3, max_length=512)
    description: str = Field(min_length=3, max_length=1024)

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    category_id: int

class CategoryDelete(BaseModel):
    id: int

class CategoryRead(BaseModel):
    id: int