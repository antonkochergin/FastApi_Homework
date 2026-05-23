from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator


class FieldValidatorsMixin:
    @field_validator("name", mode="before")
    @staticmethod
    def validate_name(value: Optional[str]) -> Optional[str]:
        if value is None:
            return value

        if not value or not value.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Name cannot be empty or whitespace",
            )

        if len(value.strip()) < 3:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Name must be at least 3 characters long",
            )

        if len(value.strip()) > 256:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Name cannot exceed 256 characters",
            )

        return value.strip()

    @field_validator("description", mode="before")
    @staticmethod
    def validate_description(value: Optional[str]) -> Optional[str]:
        if value is None:
            return value

        if not value or not value.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Description cannot be empty or whitespace",
            )

        return value.strip()

    @field_validator("slug", mode="before")
    @staticmethod
    def validate_slug(value: Optional[str]) -> Optional[str]:
        if value is None:
            return value

        if not value or not value.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Slug cannot be empty or whitespace",
            )

        if len(value.strip()) < 3:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Slug must be at least 3 characters long",
            )

        if len(value.strip()) > 64:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Slug cannot exceed 64 characters",
            )

        import re

        pattern = r"^[a-zA-Z0-9_-]+$"
        if not re.match(pattern, value.strip()):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Slug can only contain letters, numbers, underscores and hyphens",
            )

        return value.strip().lower()


class CategoryCreate(FieldValidatorsMixin, BaseModel):
    name: str
    description: str
    slug: str
    is_published: bool = True


class CategoryResponse(CategoryCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CategoryUpdate(FieldValidatorsMixin, BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    is_published: Optional[bool] = None
