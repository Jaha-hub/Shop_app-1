from enum import Enum

from pydantic import BaseModel, Field

class OrderStatusEnum(Enum):
    new = "New"
    paid = "Paid"
    complete = "Complete"
    canceled = "Canceled"


class OrderBase(BaseModel):
    user_id: int
    status: str = Field(max_length=20)
    address: str = Field(max_length=512)
    comment: str
    phone: str = Field(max_length=20)


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    pass

class OrderUpdateStatus(BaseModel):
    status: str = Field(max_length=20)


class OrderRead(BaseModel):
    id: int


class OrderProductBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price: float


class OrderProductCreate(OrderProductBase):
    pass


class OrderProductUpdate(OrderProductBase):
    pass


class OrderProductRead(OrderProductBase):
    id: int
