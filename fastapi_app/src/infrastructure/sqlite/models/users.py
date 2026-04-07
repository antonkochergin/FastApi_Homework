from fastapi_app.src.infrastructure.sqlite.database import Base
from sqlalchemy import String, Boolean, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, MappedColumn
from datetime import datetime


class User(Base):
    __tablename__ = 'auth_user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    password: Mapped[str] = mapped_column(String(120), nullable=False) #128
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    username: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    last_name: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    email: Mapped[str] = mapped_column(String, nullable=False, default="")
    date_joined: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_staff: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    # phone_number: Mapped[str | None] = mapped_column(String(20), nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"