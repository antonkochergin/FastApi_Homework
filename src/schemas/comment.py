from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator


class TextValidatorMixin:
    @field_validator("text", mode="before")
    @staticmethod
    def validate_text(value: Optional[str]) -> Optional[str]:
        if value is None:
            return value

        if not value or not value.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Name cannot be empty or whitespace",
            )

        return value.strip()


class CommentCreate(BaseModel, TextValidatorMixin):
    text: str
    post_id: int


class CommentResponse(CommentCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CommentUpdate(BaseModel, TextValidatorMixin):
    text: Optional[str] = None
