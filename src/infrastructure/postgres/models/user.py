from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .comment import Comment
    from .post import Post


class User(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        unique=True,
        # index используется для быстрого поиска в бд по данному полю
        index=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        server_default="0",  # для sqlite
    )
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)

    posts: Mapped[List["Post"]] = relationship(
        "Post", back_populates="author", cascade="all, delete-orphan"
    )
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="author", cascade="all, delete-orphan"
    )
