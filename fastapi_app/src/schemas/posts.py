from pydantic import BaseModel, Field, ConfigDict, validator
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    """Базовая модель поста - общие поля"""
    title: str = Field(..., min_length=3, max_length=256, description="Заголовок")
    text: str = Field(..., description="Текст поста")
    pub_date: datetime = Field(..., description="Дата публикации")
    is_published: bool = Field(True, description="Опубликовано")
    # Внешние ключи - часть сущности
    author_id: int = Field(..., description="ID автора")
    category_id: Optional[int] = Field(None, description="ID категории")
    location_id: Optional[int] = Field(None, description="ID локации")
    image: Optional[str] = Field(None, max_length=100, description="URL изображения")


class PostCreate(BaseModel):
    """Для создания поста - все поля кроме author_id (берется из контекста)"""
    title: str = Field(..., min_length=3, max_length=256, description="Заголовок")
    text: str = Field(..., description="Текст поста")
    pub_date: datetime = Field(..., description="Дата публикации")
    is_published: bool = Field(True, description="Опубликовано")
    category_id: Optional[int] = Field(None, description="ID категории")
    location_id: Optional[int] = Field(None, description="ID локации")
    image: Optional[str] = Field(None, max_length=100, description="URL изображения")

    @validator('is_published', pre=True)
    def prevent_string_conversion(cls, v):
        """Запретить автоматическую конвертацию строк в булевы значения"""
        if isinstance(v, str):
            raise ValueError('Must be a boolean, not a string')
        return v

    @validator('category_id', 'location_id')
    def prevent_bool_for_int(cls, v):
        """Запретить булевы значения для числовых полей"""
        if v is not None and isinstance(v, bool):
            raise ValueError('Must be an integer or null, not boolean')
        return v


class PostUpdate(BaseModel):
    """Для обновления поста - все поля опциональны"""
    title: Optional[str] = Field(None, min_length=3, max_length=256, description="Заголовок")
    text: Optional[str] = Field(None, description="Текст поста")
    pub_date: Optional[datetime] = Field(None, description="Дата публикации")
    is_published: Optional[bool] = Field(None, description="Опубликовано")
    category_id: Optional[int] = Field(None, description="ID категории")
    location_id: Optional[int] = Field(None, description="ID локации")
    image: Optional[str] = Field(None, max_length=100, description="URL изображения")

    @validator('is_published', pre=True)
    def prevent_string_conversion(cls, v):
        """Запретить автоматическую конвертацию строк в булевы значения"""
        if isinstance(v, str):
            raise ValueError('Must be a boolean, not a string')
        return v

    @validator('category_id', 'location_id')
    def prevent_bool_for_int(cls, v):
        """Запретить булевы значения для числовых полей"""
        if v is not None and isinstance(v, bool):
            raise ValueError('Must be an integer or null, not boolean')
        return v


class Post(PostBase):
    """Для чтения поста из БД"""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)