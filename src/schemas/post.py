from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, field_validator


class TitleValidatorMixin:
    @field_validator("title", mode="before")
    @staticmethod
    def validate_title(title: str):
        if title is None:
            return title

        if not title or not title.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Title cannot be empty or whitespace",
            )

        stripped = title.strip()

        if len(stripped) < 3:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Title must be at least 3 characters long",
            )

        if len(stripped) > 256:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Title cannot exceed 256 characters",
            )

        return stripped


class PostCreate(BaseModel, TitleValidatorMixin):
    title: str
    text: Optional[str] = None
    pub_date: datetime
    location_id: int
    category_id: int
    # image: Optional[str] = None
    is_published: bool = True


class PostResponse(PostCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class PostUpdate(BaseModel, TitleValidatorMixin):
    title: Optional[str] = Field(default=None)
    text: Optional[str] = None
    pub_date: Optional[datetime] = None
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    # image: Optional[str] = None
    is_published: Optional[bool] = None


class PostImageResponse(BaseModel):
    image_path: str
