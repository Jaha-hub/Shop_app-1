from sqlalchemy import Column, String

from app.core.models import Base, IntIdMixin, TimeActionMixin


class Category(Base, IntIdMixin, TimeActionMixin):
     __tablename__ = 'categories'

     """
     Моделька категории

     Attributes:
          id: уникальной идентификатор
          name: название категории
          description: описание категории
          created_at: временная отметка создания категории
          updated_at: временная отметка обновления категории
     """

     name = Column(String(512), nullable=False)
     description = Column(String(1024), nullable=True)
