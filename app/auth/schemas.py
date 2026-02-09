import re
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator

from app.auth.validators import validate_password


class RoleEnum(str, Enum):
    admin = "admin"
    client = "client"
    moderator = "moderator"



class UserBase(BaseModel):
    """
    Базовая Pydantic моделька пользователя

    Attributes:
        username: имя пользователя
        email: почта пользователя
        fullname: полное имя пользователя
    """
    username: str = Field(min_length=3, max_length=320)
    email: EmailStr
    fullname: str = Field(min_length=3, max_length=512)


    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:

        """
        Функция для валидации имени пользователя

        Проверка на то что имя пользователя начинается с буквы
        Проверка на то что имя пользователя содержит только буквы, цифры и _

        :param value: значение имени пользователя
        :return: валидированное имя пользователя
        """

        if not re.fullmatch(r'^[A-Za-z][A-Za-z0-9_]*$', value):
            raise ValueError("Имя пользователя должно содержать только буквы, цифры и _")

        return value.lower()


class UserRegister(UserBase):

    """
    Pydantic моделька для регистрации пользователя

    Attributes:
        password: пароль пользователя
        username: имя пользователя
        email: почта пользователя
        fullname: полное имя пользователя
    """

    password: str

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, value):

        """
        Метод валидации пароля
        """

        return validate_password(value)


class UserCreate(UserRegister):
    """
    Pydantic моделька для создания пользователя

    Attributes:
        role: роль пользователя
        password: пароль пользователя
        username: имя пользователя
        email: почта пользователя
        fullname: полное имя пользователя
    """
    role: RoleEnum


class UserUpdate(UserBase):
    """
    Базовая Pydantic моделька для обновления пользователя

    Attributes:
        username: имя пользователя
        email: почта пользователя
        fullname: полное имя пользователя
    """
    pass

class UserAdminUpdate(UserBase):
    """
    Pydantic моделька для обновления пользователя админом

    Attributes:
        role: роль пользователя
        is_active: флажок активность
        username: имя пользователя
        email: почта пользователя
        fullname: полное имя пользователя
    """

    role: RoleEnum
    is_active: bool


class ChangePasswordSchema(BaseModel):
    """
    Pydantic моделька для изменения пароля

    Attributes:
        old_password: старый пароль
        new_password: новый пароль
    """

    old_password: str
    new_password: str

    @field_validator( "new_password", mode="before")
    @classmethod
    def validate_password(cls, value):
        """
        Метод валидации пароля
        """

        return validate_password(value)


    @model_validator(mode="after")
    def check_password_match(self):
        if self.old_password == self.new_password:
            raise ValueError("Пароли не должны совпадать")
        return self


class UserRead(UserBase):
    """
    Pydantic моделька для просмотра пользователя

    Attributes:
        id: ИД пользователя
        role: роль пользователя
        username: имя пользователя
        email: почта пользователя
        fullname: полное имя пользователя
        is_active: флажок активность
        created_at: временная отметка создания пользователя
        updated_at: временная отметка обновления пользователя
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


class RefreshToken(BaseModel):
    refresh_token: str