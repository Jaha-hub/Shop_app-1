from sqlalchemy import Column, String, Text, Numeric, BigInteger, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.models import IntIdMixin, TimeActionMixin, Base


class Product(Base, IntIdMixin, TimeActionMixin):
    """
    Моделька продукта

    Attributes:
         id: уникальной идентификатор
         name: название продукта
         short_description: краткое описание продукта
         long_description: длинное описание продукта
         price: цена продукта
         category_id: Ид категории продукта
         created_at: временная отметка создания продукта
         updated_at: временная отметка обновления продукта
        """

    __tablename__ = "products"

    name = Column(String(512), nullable=False)
    short_description = Column(String(512), nullable=False)
    long_description = Column(Text, nullable=True)
    price = Column(Numeric(20, 2), nullable=False)
    category_id = Column(BigInteger, ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False)

    characteristics = relationship("ProductCharacteristics", backref="product", lazy="selectin")
    reviews = relationship("ProductReview", backref="product", lazy="selectin")



class ProductCharacteristics(Base, IntIdMixin):
    """
    Моделька характеристики продукта

    Attributes:
         id: уникальной идентификатор
         name: название характеристики
         value: значение характеристики
         product_id: Ид продукта

    """

    __tablename__ = "product_characteristics"

    name = Column(String(512), nullable=False)
    value = Column(String(512), nullable=False)
    product_id = Column(BigInteger, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)


# class ProductImage(Base, IntIdMixin):
#     __tablename__ = "product_images"


class ProductReview(Base, IntIdMixin, TimeActionMixin):
    """
    Моделька отзыва продукта

    Attributes:
         id: уникальной идентификатор
         user_id: ИД пользователя
         product_id: ИД продукта
         message: текст отзыва
         grade: оценка отзыва
         created_at: временная отметка создания отзыва
         updated_at: временная отметка обновления отзыва
    """

    __tablename__ = "product_reviews"

    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(BigInteger, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    message = Column(String(2048), nullable=False)
    grade = Column(Integer, nullable=False)


