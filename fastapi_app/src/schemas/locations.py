from pydantic import BaseModel, Field, ConfigDict, validator
from datetime import datetime
from typing import Optional


class LocationBase(BaseModel):
    """Базовая модель локации"""
    name: str = Field(..., max_length=256, description="Название локации")
    is_published: bool = Field(True, description="Опубликовано")

    @validator('name')
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Location name cannot be empty')
        return v.strip()


class LocationCreate(LocationBase):
    """Для создания локации"""
    @validator('is_published', pre=True)
    def prevent_string_conversion(cls, v):
        if isinstance(v, str):
            raise ValueError('Must be a boolean, not a string')
        if isinstance(v, int) and not isinstance(v, bool):
            raise ValueError('Must be a boolean, not an integer')
        return v


class LocationUpdate(BaseModel):
    """Для обновления локации - все поля опциональны"""
    name: Optional[str] = Field(None, max_length=256, description="Название локации")
    is_published: Optional[bool] = Field(None, description="Опубликовано")

    @validator('name')
    def name_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Location name cannot be empty')
        return v.strip() if v else v

    @validator('is_published', pre=True)
    def prevent_string_conversion(cls, v):
        if v is not None:
            if isinstance(v, str):
                raise ValueError('Must be a boolean, not a string')
            if isinstance(v, int) and not isinstance(v, bool):
                raise ValueError('Must be a boolean, not an integer')
        return v


class Location(LocationBase):
    """Для чтения локации из БД"""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)