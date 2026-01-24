from datetime import datetime
from enum import Enum
import re
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator

from app.auth.validators import validate_passwords


class UserBase(BaseModel):
    """
    pydantic Моделька пользователя


    Attributes:
        email: Почта пользователя
        full_name: Полное имя пользователя
        username: имя пользователя
    """

    email: EmailStr
    full_name: str = Field(min_length=3, max_length=512)
    username: str = Field(min_length=3, max_length=320)

    @field_validator('username')
    @classmethod
    def validate_username(cls, value: str) -> str:
        """
        функция для валидации имени пользователя

        Начинается с буквы,
        может содержать буквы и цифры


        :param value: значение для валедации
        :return: имя пользователя
        """
        if re.fullmatch(
                r'^[A-Za-z][A-Za-z0-9_]*$',
                value
        ):
            raise ValueError('Username cannot contain special characters')

        return value.lower()


class UserRegister(UserBase):
    """
    Pydantic Моделька для регистрации
    Attributes:
        password: Пароль
        email: Почта пользователя
        full_name: Полное имя пользователя
        username: имя пользователя
    """

    password: str

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, value):
        """
        Метод валидации пароля
        Пароль должен состоять из строчных и заглавных букв цифр и спец символов

        :param value: значение
        :return: значение
        """

        return validate_passwords(value)


class RoleEnum(str, Enum):
    admin = "admin"
    client = "client"
    moderator = "moderator"


class UserCreate(UserRegister):
    """
    Pydantic Моделька для создания пользователя

    Attributes:
        role: Роль пользователя
        password: Пароль
        email: Почта пользователя
        full_name: Полное имя пользователя
        username: имя пользователя
    """

    role: RoleEnum


class UserUpdate(UserBase):
    """
    Pydantic Моделька для обнавление пользователя

    Attributes:
        email: Почта пользователя
        full_name: Полное имя пользователя
        username: имя пользователя


    """

    pass


class UserAdminUpdate(UserBase):
    """
    Pydantic Моделька для обнавление пользователя

    Attributes:
        email: Почта пользователя
        full_name: Полное имя пользователя
        username: имя пользователя
        role: Роль
        is_active: флажок активности


    """
    role: RoleEnum
    is_active: bool


class ChengePasswordSchemas(BaseModel):
    """
    Pydantic моделька для мены пароля

    """

    old_password: str
    new_password1: str

    @field_validator("new_password1", mode="before")
    @classmethod
    def validate_password(cls, value):
        """
        Метод валидации пароля
        Пароль должен состоять из строчных и заглавных букв цифр и спец символов

        :param value: значение
        :return: значение
        """

        return validate_passwords(value)

    @model_validator(mode="after")
    def check_password_match(self):
        if self.old_password == self.new_password1:
            raise ValueError("Пароли не должны совпадать")
        return self


class UserRead(UserBase):
    """
    Pydantic моделька для просмотра Пользователя

    Attributes:
        email: Почта пользователя
        full_name: Полное имя пользователя
        username: имя пользователя
        role: Роль
        is_active: флажок активности

        created_at: Создание пользователя
        updated_at: Обнавление Пользователя
    """

    id: int
    role: RoleEnum
    is_active: bool

    created_at: datetime
    updated_at: datetime | None = None



class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"