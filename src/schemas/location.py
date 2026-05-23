from datetime import datetime

from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator


class LocationCreate(BaseModel):
    name: str
    is_published: bool = True

    @field_validator("name", mode="before")
    @staticmethod
    def validate_name(name: str):
        if name is None:
            return name

        if not name or not name.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Name cannot be empty or whitespace",
            )

        stripped = name.strip()

        if len(stripped) < 3:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Name must be at least 3 characters long",
            )

        if len(stripped) > 256:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Name cannot exceed 256 characters",
            )

        return stripped


class LocationResponse(LocationCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
