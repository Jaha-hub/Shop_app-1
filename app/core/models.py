from datetime import datetime

from sqlalchemy import Column, BigInteger, DateTime
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class IntIdMixin:
    """
    Класс миксин для добавления поле ID в виде целых чисел
    """

    id = Column(BigInteger, primary_key=True, autoincrement=True)

class TimeActionMixin:
    """
    Класс миксин для добовление полей создание и обновление
    """

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)