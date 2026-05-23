from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.postgres.database import Base


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        primary_key=True,
        # index=True, # pk автоматически создает index
        autoincrement=True,
    )


class PublishStatusMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    is_published: Mapped[bool] = mapped_column(default=True, nullable=False)
