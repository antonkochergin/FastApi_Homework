
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    """Базовая модель поста"""
    title: str = Field(max_length=256,description="Заголовок")
    text: str = Field(description="Текст поста")
    pub_date: datetime = Field(description="Дата публикации ")
    author_id: int = Field(description="ID автора")
    location_id: Optional[int] = Field(None, description="ID локации")
    category_id: int = Field(description="ID категории")
    image: Optional[str] = Field(None, description="URL изображения")
    is_published: bool = Field(True, description="Опубликовано")

    model_config = ConfigDict(from_attributes=True)