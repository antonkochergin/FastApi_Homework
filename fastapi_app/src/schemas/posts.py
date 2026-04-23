from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from src.schemas.users import User
from src.schemas.categories import Category
from src.schemas.locations import Location
from src.core.exceptions.domain_exceptions import (
    PostTitleEmptyException,
    PostTextEmptyException
)


class PostBase(BaseModel):
    """Базовая модель поста"""
    title: str = Field(max_length=256)
    text: str
    pub_date: datetime
    author_id: int
    category_id: int | None = None
    location_id: int | None = None
    image: str | None = None
    is_published: bool = True

    @field_validator("title")
    @classmethod
    def validate_title_not_empty(cls, v: str) -> str:
        """Проверка, что заголовок поста не состоит только из пробелов"""
        if not v or not v.strip():
            raise ValueError(PostTitleEmptyException().get_detail())
        return v.strip()

    @field_validator("text")
    @classmethod
    def validate_text_not_empty(cls, v: str) -> str:
        """Проверка, что содержание поста не состоит только из пробелов"""
        if not v or not v.strip():
            raise ValueError(PostTextEmptyException().get_detail())
        return v.strip()


class PostCreate(PostBase):
    """Для создания поста"""
    pass


class PostUpdate(BaseModel):
    """Для обновления поста - все поля необязательные"""
    title: str | None = Field(None, max_length=256)
    text: str | None = None
    pub_date: datetime | None = None
    author_id: int | None = None
    category_id: int | None = None
    location_id: int | None = None
    image: str | None = None
    is_published: bool | None = None

    @field_validator("title")
    @classmethod
    def validate_title_not_empty(cls, v: str | None) -> str | None:
        """Проверка, что заголовок поста не состоит только из пробелов"""
        if v is not None and (not v or not v.strip()):
            raise ValueError(PostTitleEmptyException().get_detail())
        return v.strip() if v else v

    @field_validator("text")
    @classmethod
    def validate_text_not_empty(cls, v: str | None) -> str | None:
        """Проверка, что содержание поста не состоит только из пробелов"""
        if v is not None and (not v or not v.strip()):
            raise ValueError(PostTextEmptyException().get_detail())
        return v.strip() if v else v


class Post(PostBase):
    """Для чтения поста из БД"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    author: User | None = None
    category: Category | None = None
    location: Location | None = None


class PostDetail(Post):
    """Детальная информация о посте со всеми связями"""
    pass