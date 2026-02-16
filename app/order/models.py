from sqlalchemy import Column, String, Text, Numeric, BigInteger, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.models import IntIdMixin, TimeActionMixin, Base


class Order(Base, IntIdMixin, TimeActionMixin):

    __tablename__ = "orders"
    user_id = Column(BigInteger,ForeignKey("users.id"), nullable=False)
    address = Column(String(512), nullable=False)
    comment = Column(Text, nullable=False)
    status = Column(String(20), nullable=False)
    phone = Column(String(20), nullable=False)

    order_products = relationship('OrderProducts', backref='order', lazy='selectin')


class OrderProducts(Base, IntIdMixin, TimeActionMixin):
    __tablename__ = "orderproducts"

    order_id = Column(BigInteger,ForeignKey("orders.id"), nullable=False)
    product_id = Column(BigInteger,ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)