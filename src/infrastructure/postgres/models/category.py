from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, PublishStatusMixin
from .post import Post


class Category(BaseModel, PublishStatusMixin):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    slug: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)

    posts: Mapped[List["Post"]] = relationship(
        "Post", back_populates="category", cascade="all, delete-orphan"
    )
