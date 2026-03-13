from pydantic import BaseModel, Field, ConfigDict , validator
from datetime import datetime
from typing import Optional

class CategoryBase(BaseModel):
    """Базовая модель категории"""
    title: str = Field(..., max_length=32, description="Название категории")  # Исправил на 32
    description: str = Field("", max_length=150, description="Описание")  # Добавил default ""
    slug: str = Field(
        max_length=32,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description="URL-идентификатор"
    )
    is_published: bool = Field(True, description="Опубликовано")


class CategoryCreate(BaseModel):
    title: str = Field(..., max_length=32)
    slug: str = Field(..., max_length=32, pattern=r'^[a-zA-Z0-9_-]+$')
    description: str = Field("", max_length=150)
    is_published: bool = Field(True)

    @validator('is_published', pre=True)
    def prevent_number_conversion(cls, v):
        """Запретить автоматическую конвертацию чисел в булевы значения"""
        if isinstance(v, int) and not isinstance(v, bool):
            raise ValueError('Must be a boolean, not an integer')
        if isinstance(v, str):
            raise ValueError('Must be a boolean, not a string')
        return v

class CategoryUpdate(BaseModel):
    """Для обновления категории - все поля опциональны"""
    title: Optional[str] = Field(None, max_length=32, description="Название категории")
    description: Optional[str] = Field(None, max_length=150, description="Описание")
    slug: Optional[str] = Field(
        None,
        max_length=32,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description="URL-идентификатор"
    )
    is_published: Optional[bool] = Field(None, description="Опубликовано")


class Category(CategoryBase):
    """Для чтения категории из БД"""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

