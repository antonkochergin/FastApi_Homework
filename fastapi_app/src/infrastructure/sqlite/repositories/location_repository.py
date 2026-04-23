from typing import Type, List
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime

from src.infrastructure.sqlite.models.location import Location
from src.schemas.locations import LocationCreate, LocationUpdate
from src.core.exceptions.database_exceptions import (
    LocationNotFoundException,
    LocationAlreadyExistsException,
    DatabaseOperationError
)


class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location

    def get_by_id(self, session: Session, location_id: int) -> Location:
        """Получить локацию по ID"""
        try:
            query = select(self._model).where(self._model.id == location_id)
            location = session.scalar(query)
            if not location:
                raise LocationNotFoundException(
                    detail=f"Локация с ID {location_id} не найдена"
                )
            return location
        except SQLAlchemyError as e:
            raise DatabaseOperationError(
                detail=f"Ошибка при получении локации: {str(e)}"
            )

    def get_by_name(self, session: Session, name: str) -> Location | None:
        """Получить локацию по названию"""
        try:
            query = select(self._model).where(self._model.name == name)
            return session.scalar(query)
        except SQLAlchemyError as e:
            raise DatabaseOperationError(
                detail=f"Ошибка при получении локации по названию: {str(e)}"
            )

    def get_all(self, session: Session) -> List[Location]:
        """Получить все локации"""
        try:
            query = select(self._model)
            return list(session.scalars(query).all())
        except SQLAlchemyError as e:
            raise DatabaseOperationError(
                detail=f"Ошибка при получении списка локаций: {str(e)}"
            )

    def get_published(self, session: Session) -> List[Location]:
        """Получить только опубликованные локации"""
        try:
            query = select(self._model).where(self._model.is_published.is_(True))
            return list(session.scalars(query).all())
        except SQLAlchemyError as e:
            raise DatabaseOperationError(
                detail=f"Ошибка при получении опубликованных локаций: {str(e)}"
            )

    def create(self, session: Session, location_data: LocationCreate) -> Location:
        """Создать новую локацию"""
        try:
            query = (
                insert(self._model)
                .values(
                    name=location_data.name,
                    is_published=location_data.is_published,
                    created_at=datetime.now()
                )
                .returning(self._model)
            )
            location = session.scalar(query)
            session.flush()
            return location
        except IntegrityError:
            raise LocationAlreadyExistsException(
                detail=f"Локация с названием '{location_data.name}' уже существует"
            )
        except SQLAlchemyError as e:
            raise DatabaseOperationError(
                detail=f"Ошибка при создании локации: {str(e)}"
            )

    def update(self, session: Session, location_id: int, location_data: LocationUpdate) -> Location:
        """Обновить локацию"""
        try:
            location = self.get_by_id(session, location_id)

            update_data = location_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(location, field):
                    setattr(location, field, value)

            session.flush()
            return location
        except IntegrityError:
            raise LocationAlreadyExistsException(
                detail=f"Локация с названием '{location_data.name}' уже существует"
            )
        except SQLAlchemyError as e:
            raise DatabaseOperationError(
                detail=f"Ошибка при обновлении локации: {str(e)}"
            )

    def delete(self, session: Session, location_id: int) -> None:
        """Удалить локацию"""
        try:
            location = self.get_by_id(session, location_id)
            session.delete(location)
            session.flush()
        except SQLAlchemyError as e:
            raise DatabaseOperationError(
                detail=f"Ошибка при удалении локации: {str(e)}"
            )