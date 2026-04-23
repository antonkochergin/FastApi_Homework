from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from src.core.exceptions.domain_exceptions import (
    CategoryTitleEmptyException,
    CategorySlugEmptyException
)


class CategoryBase(BaseModel):
    """Базовая модель категории"""
    title: str = Field(max_length=256)
    description: str
    slug: str = Field(
        max_length=64,
        pattern=r'^[a-zA-Z0-9_-]+$'
    )
    is_published: bool = True

    @field_validator("title")
    @classmethod
    def validate_title_not_empty(cls, v: str) -> str:
        """Проверка, что название категории не состоит только из пробелов"""
        if not v or not v.strip():
            raise ValueError(CategoryTitleEmptyException().get_detail())
        return v.strip()

    @field_validator("slug")
    @classmethod
    def validate_slug_not_empty(cls, v: str) -> str:
        """Проверка, что slug категории не состоит только из пробелов"""
        if not v or not v.strip():
            raise ValueError(CategorySlugEmptyException().get_detail())
        return v.strip().lower()


class CategoryCreate(CategoryBase):
    """Для создания категории"""
    pass


class CategoryUpdate(BaseModel):
    """Для обновления категории"""
    title: str | None = Field(None, max_length=256)
    description: str | None = None
    slug: str | None = Field(None, max_length=64, pattern=r'^[a-zA-Z0-9_-]+$')
    is_published: bool | None = None

    @field_validator("title")
    @classmethod
    def validate_title_not_empty(cls, v: str | None) -> str | None:
        """Проверка, что название категории не состоит только из пробелов"""
        if v is not None and (not v or not v.strip()):
            raise ValueError(CategoryTitleEmptyException().get_detail())
        return v.strip() if v else v

    @field_validator("slug")
    @classmethod
    def validate_slug_not_empty(cls, v: str | None) -> str | None:
        """Проверка, что slug категории не состоит только из пробелов"""
        if v is not None and (not v or not v.strip()):
            raise ValueError(CategorySlugEmptyException().get_detail())
        return v.strip().lower() if v else v


class Category(CategoryBase):
    """Для чтения категории из БД"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime