from pydantic import BaseModel, Field, ConfigDict

class CategoryBase(BaseModel):
    """Базовая модель категории"""

    title: str = Field(max_length=256, description="Название категории")
    description: str = Field(description="Описание")
    slug: str = Field(
        max_length=64,
        pattern=r'^[a-zA-Z0-9_-]+$'
    )
    is_published: bool = Field(True, description="Опубликовано")

class Category(CategoryBase):
    """Полная модель категории с id"""
    id:int | None = None
    model_config = ConfigDict(from_attributes=True)