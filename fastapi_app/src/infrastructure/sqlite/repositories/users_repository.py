from typing import Type
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from src.infrastructure.sqlite.models.users import User
from src.schemas.users import UserCreate, UserUpdate
from src.core.exceptions.database_exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException
)


class UsersRepository:
    def __init__(self):
        self._model: Type[User] = User

    def get_by_id(self, session: Session, user_id: int) -> User:
        query = (
            select(self._model)
            .where(self._model.id == user_id)
        )
        user = session.scalar(query)
        if not user:
            raise UserNotFoundException()
        return user

    def get_by_username(self, session: Session, username: str) -> User | None:
        query = (
            select(self._model)
            .where(self._model.username == username)
        )
        return session.scalar(query)

    def get_by_email(self, session: Session, email: str) -> User | None:
        query = (
            select(self._model)
            .where(self._model.email == email)
        )
        return session.scalar(query)

    def get_all(self, session: Session) -> list[User]:
        query = select(self._model)
        return list(session.scalars(query).all())

    def create(self, session: Session, user_data: UserCreate) -> User:
        query = (
            insert(self._model)
            .values(
                username=user_data.username,
                email=user_data.email or "",
                password=user_data.password,
                first_name=user_data.first_name or "",
                last_name=user_data.last_name or "",
                is_active=user_data.is_active,
                is_superuser=False,
                is_staff=False,
                date_joined=datetime.now(),
                last_login=None
            )
            .returning(self._model)
        )
        try:
            user = session.scalar(query)
            session.flush()
            return user
        except IntegrityError:
            raise UserAlreadyExistsException()

    def update(self, session: Session, user_id: int, user_data: UserUpdate) -> User:
        user = self.get_by_id(session, user_id)

        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(user, field) and field not in ['id', 'date_joined']:
                setattr(user, field, value)

        session.flush()
        return user

    def delete(self, session: Session, user_id: int) -> None:
        user = self.get_by_id(session, user_id)
        session.delete(user)
        session.flush()