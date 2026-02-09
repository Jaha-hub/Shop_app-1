from sqlalchemy import Column, String, Text, Boolean

from app.core.models import Base, IntIdMixin, TimeActionMixin


class User(Base, IntIdMixin,TimeActionMixin):
    """
    Моделька пользователя

    Attributes:
        id: уникальной идентификатор
        email: почта пользователя
        fullname: полное имя пользователя
        role: роль пользователя
        username: уникальное имя пользователя
        hashed_password: хэшированный пароль
        is_active: флажок активности пользователя
        created_at: временная отметка создания пользователя
        updated_at: временная отметка обновления пользователя
    """

    __tablename__ = "users"

    email = Column(String(320), nullable=False, unique=True)
    fullname = Column(String(512), nullable=False)
    role = Column(String(20), nullable=False, default="client")
    username = Column(String(320), nullable=False, unique=True)
    hashed_password = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
