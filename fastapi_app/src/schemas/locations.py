from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from src.core.exceptions.domain_exceptions import LocationNameEmptyException


class LocationBase(BaseModel):
    """Базовая модель местоположения"""
    name: str = Field(max_length=256)
    is_published: bool = True

    @field_validator("name")
    @classmethod
    def validate_name_not_empty(cls, v: str) -> str:
        """Проверка, что название локации не состоит только из пробелов"""
        if not v or not v.strip():
            raise ValueError(LocationNameEmptyException().get_detail())
        return v.strip()


class LocationCreate(LocationBase):
    """Для создания новой локации"""
    pass


class LocationUpdate(BaseModel):
    """Для обновления локации - все поля необязательные"""
    name: str | None = Field(None, max_length=256)
    is_published: bool | None = None

    @field_validator("name")
    @classmethod
    def validate_name_not_empty(cls, v: str | None) -> str | None:
        """Проверка, что название локации не состоит только из пробелов"""
        if v is not None and (not v or not v.strip()):
            raise ValueError(LocationNameEmptyException().get_detail())
        return v.strip() if v else v


class Location(LocationBase):
    """Для чтения локации из БД"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime