from pydantic import BaseModel, Field, ConfigDict, validator
from datetime import datetime
from typing import Optional


class CommentBase(BaseModel):
    """Базовая модель комментария"""
    text: str = Field(..., min_length=1, max_length=1000, description="Текст комментария")
    post_id: int = Field(..., description="ID поста")
    author_id: int = Field(..., description="ID автора")


class CommentCreate(BaseModel):
    """Для создания комментария"""
    text: str = Field(..., min_length=1, max_length=1000, description="Текст комментария")
    post_id: int = Field(..., description="ID поста")
    author_id: int = Field(..., description="ID автора")

    @validator('text')
    def text_not_empty(cls, v):
        """Проверка что текст не пустой и не состоит из пробелов"""
        if not v or not v.strip():
            raise ValueError('Comment text cannot be empty')
        return v.strip()


class CommentUpdate(BaseModel):
    """Для обновления комментария"""
    text: Optional[str] = Field(None, min_length=1, max_length=1000, description="Текст комментария")

    @validator('text')
    def text_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Comment text cannot be empty')
        return v.strip() if v else v


class Comment(CommentBase):
    """Для чтения комментария из БД"""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)