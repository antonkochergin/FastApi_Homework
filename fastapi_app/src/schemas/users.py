from datetime import datetime
from pydantic import ConfigDict, BaseModel, Field, EmailStr, validator
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=150)
    password: str = Field(..., min_length=8)
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=128)
    last_name: Optional[str] = Field(None, max_length=128)
    age: Optional[int] = Field(None, ge=0, le=150)
    is_active: bool = True

    @validator('age', pre=True)
    def validate_age(cls, v):
        """Проверка что age это число, а не строка"""
        if v is not None:
            if isinstance(v, str):
                if not v.isdigit():
                    raise ValueError('Age must be a number')
                return int(v)
            if isinstance(v, bool):
                raise ValueError('Age must be a number, not boolean')
        return v

    @validator('is_active', pre=True)
    def prevent_string_conversion(cls, v):
        """Запретить автоматическую конвертацию строк в булевы значения"""
        if isinstance(v, str):
            raise ValueError('Must be a boolean, not a string')
        if isinstance(v, int) and not isinstance(v, bool):
            raise ValueError('Must be a boolean, not an integer')
        return v

class UserBase(BaseModel):
    """Базовая модель пользователя - общие поля для всех схем"""
    username: str = Field(min_length=3, max_length=150)
    email: str | None = Field(None, max_length=254)
    first_name: str | None = Field(None, max_length=128)  # В модели max_length=128
    last_name: str | None = Field(None, max_length=128)   # В модели max_length=128
    is_active: bool = True


class UserUpdate(BaseModel):
    """Для обновления пользователя все поля необязательные"""
    username: str | None = Field(None, min_length=3, max_length=150)
    password: str | None = Field(None, min_length=8, max_length=128)
    email: EmailStr | None = None
    first_name: str | None = Field(None, max_length=128)
    last_name: str | None = Field(None, max_length=128)
    is_active: bool | None = None
    is_staff: bool | None = None
    is_superuser: bool | None = None


class User(UserBase):
    """Для чтения пользователя из БД (без пароля) - полная модель"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_superuser: bool
    is_staff: bool
    date_joined: datetime
    last_login: datetime | None = None
    email: str | None = None  # Переопределяем, т.к. в БД это строка, а не EmailStr
