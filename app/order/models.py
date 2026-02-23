from sqlalchemy import Column, String, Text, Numeric, BigInteger, ForeignKey, Integer, UniqueConstraint, select, func, \
    Float
from sqlalchemy.orm import relationship

from sqlalchemy.ext.hybrid import hybrid_property

from app.core.models import IntIdMixin, TimeActionMixin, Base


class Order(Base, IntIdMixin, TimeActionMixin):

    __tablename__ = "orders"
    user_id = Column(BigInteger,ForeignKey("users.id"), nullable=False)
    address = Column(String(512), nullable=False)
    comment = Column(Text, nullable=False)
    status = Column(String(20), nullable=False)
    phone = Column(String(20), nullable=False)

    products = relationship(
        "OrderProducts",
        backref="order",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    @hybrid_property
    def total_sum(self):
        return sum(product.quantity * product.price for product in self.products)

    @total_sum.expression
    def total_sum(self):
        return (
            select(
                func.sum(OrderProducts.quantity * OrderProducts.price).where(OrderProducts.order_id == self.id).scalar_subquery()
            )
        )



class OrderProducts(Base, IntIdMixin, TimeActionMixin):
    __tablename__ = "order_products"

    order_id = Column(BigInteger,ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(BigInteger,ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    __table_args__ = (
        UniqueConstraint('order_id', 'product_id', name='unique_product_id'),
    )