from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class OrderProductBase(BaseModel):
    product_id: int
    quantity: float = Field(ge=0.1)
    price: float = Field(ge=0)


class OrderProductCreate(OrderProductBase):
    pass


class OrderProductUpdate(OrderProductBase):
    pass


class OrderProductRead(OrderProductBase):
    id: int


class OrderStatusEnum(Enum):
    new = "New"
    paid = "Paid"
    complete = "Complete"
    canceled = "Canceled"


class OrderBase(BaseModel):
    status: OrderStatusEnum = OrderStatusEnum.new
    address: str = Field(max_length=512)
    comment: str
    phone: str = Field(max_length=20)


class OrderCreate(OrderBase):
    products: List[OrderProductCreate]


class OrderUpdate(OrderBase):
    products: List[OrderProductUpdate]


class OrderUpdateStatus(BaseModel):
    status: OrderStatusEnum = OrderStatusEnum.new


class OrderRead(OrderBase):
    id: int
    user_id: int
    products: List[OrderProductRead]
    total_sum: float = Field(ge=0)