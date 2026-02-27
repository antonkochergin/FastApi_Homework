from pydantic import BaseModel, Field
from datetime import datetime

class Comment(BaseModel):
    """Базовая модель комментария"""
    text: str = Field(max_length=1000, description="Текст комментария")
    post_id: int = Field(description="ID поста")
    author_id: int = Field(description="ID автора")
    created_at: datetime = Field(default_factory=datetime.now, frozen=True)