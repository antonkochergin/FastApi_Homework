from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from src.core.exceptions.domain_exceptions import CommentTextEmptyException


class CommentBase(BaseModel):
    """Базовая модель комментария"""
    text: str = Field(min_length=1, description="Текст комментария")
    post_id: int = Field(description="ID поста, к которому относится комментарий")
    author_id: int = Field(description="ID автора комментария")

    @field_validator("text")
    @classmethod
    def validate_text_not_empty(cls, v: str) -> str:
        """Проверка, что текст комментария не состоит только из пробелов"""
        if not v or not v.strip():
            raise ValueError(CommentTextEmptyException().get_detail())
        return v.strip()


class CommentCreate(CommentBase):
    """Для создания комментария"""
    pass


class CommentUpdate(BaseModel):
    """Для обновления комментария - только текст можно менять"""
    text: str = Field(min_length=1, description="Новый текст комментария")

    @field_validator("text")
    @classmethod
    def validate_text_not_empty(cls, v: str) -> str:
        """Проверка, что текст комментария не состоит только из пробелов"""
        if not v or not v.strip():
            raise ValueError(CommentTextEmptyException().get_detail())
        return v.strip()


class Comment(CommentBase):
    """Для чтения комментария из БД"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime