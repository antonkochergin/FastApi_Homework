from fastapi_app.src.infrastructure.sqlite.database import Base
from sqlalchemy import String, Boolean, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, MappedColumn
from datetime import datetime

class User(Base):
    __tablename__ = "auth_users"


    id: Mapped[int] = mapped_column(Integer,primary_key=True )
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    username: Mapped[str] = mapped_column(String(150), primary_key=True, )
    first_name: Mapped[str] = mapped_column(String(128), default="")
    last_name:Mapped[str] = mapped_column(String(128), default="")
    email: Mapped[str] = mapped_column(String , default="")
    date_joined: Mapped[datetime] = mapped_column(DateTime)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active:Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser:Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"