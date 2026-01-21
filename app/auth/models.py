from sqlalchemy import BigInteger, Column, DateTime, String, Text, Boolean

from app.core.models import Base, IntIdMixin, TimeActionMixin



class User(Base, IntIdMixin, TimeActionMixin):
    """

    Attributes:
        id (int): Уникальный идефикатор
        email (str): Почта пользователоя
        fullname: Полное имя
        role: роль
        username: уникальное имя Пользователя
        hashed_password: хешированный пороль
        is_active: флажог активность
        created_at: время создания
        updated_at: временая отметка обновления пользователя
    """
    __tablename__ = 'users'

    email = Column(String(320), unique=True, nullable=False)
    fullname = Column(String(512), nullable=False)
    role = Column(String(20), nullable=False, default='client')
    username = Column(String(320),unique=True, nullable=False)
    hashed_password = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)