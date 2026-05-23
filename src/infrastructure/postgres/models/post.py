from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, PublishStatusMixin
from .user import User

if TYPE_CHECKING:
    from .category import Category
    from .comment import Comment
    from .location import Location


class Post(BaseModel, PublishStatusMixin):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    pub_date: Mapped[datetime] = mapped_column(nullable=False)
    image: Mapped[str | None] = mapped_column(nullable=True)

    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="post")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id"), nullable=False, index=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False, index=True
    )

    author: Mapped["User"] = relationship("User", back_populates="posts")
    location: Mapped["Location"] = relationship("Location", back_populates="posts")
    category: Mapped["Category"] = relationship("Category", back_populates="posts")
