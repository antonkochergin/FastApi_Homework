from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, PublishStatusMixin
from .post import Post


class Location(BaseModel, PublishStatusMixin):
    __tablename__ = "locations"

    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)

    posts: Mapped[List["Post"]] = relationship(
        "Post", back_populates="location", cascade="all, delete-orphan"
    )
