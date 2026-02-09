from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class IntIdMixin:
    """
    Класс миксин для добавления поля ид в виде целых чисел
    """
    id = Column(BigInteger, primary_key=True, autoincrement=True)


class TimeActionMixin:
    """
    Класс миксин для добавления полей с временной отметкой создания и обновления
    """
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


