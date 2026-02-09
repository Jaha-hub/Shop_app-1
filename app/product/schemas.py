
from pydantic import BaseModel, Field

from app.core.schemas import TimeActionSchema


class ProductCharacteristicsBase(BaseModel):
    name: str = Field(max_length=512)
    value: str = Field(max_length=512)


class ProductCharacteristicsCreate(ProductCharacteristicsBase):
    pass


class ProductCharacteristicsUpdate(ProductCharacteristicsBase):
    pass


class ProductCharacteristicsRead(ProductCharacteristicsBase):
    id: int



class ProductReviewBase(BaseModel):
    message: str = Field(max_length=2048)
    grade: int = Field(ge=0, le=5)


class ProductReviewCreate(ProductReviewBase):
    pass


class ProductReviewUpdate(ProductReviewBase):
    pass


class ProductReviewRead(ProductReviewBase, TimeActionSchema):
    id: int
    user_id: int



class ProductBase(BaseModel):
    name: str = Field(max_length=512)
    short_description: str = Field(max_length=512)
    price: float = Field(max_digits=20, decimal_places=2)

class ProductCreate(ProductBase):
    category_id: int = Field(ge=1)
    long_description: str


class ProductUpdate(ProductBase):
    long_description: str


class ProductMinRead(ProductBase):
    id: int
    rating: float = 0
    review_count: int = 0


class ProductRead(ProductMinRead, TimeActionSchema):
    category_id: int = Field(ge=1)
    long_description: str

    reviews: list[ProductReviewRead]
    characteristics: list[ProductCharacteristicsRead]
