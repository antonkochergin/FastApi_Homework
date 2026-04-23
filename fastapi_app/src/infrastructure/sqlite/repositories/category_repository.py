from typing import Type, List
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime

from src.infrastructure.sqlite.models.category import Category
from src.schemas.categories import CategoryCreate, CategoryUpdate
from src.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    CategoryAlreadyExistsException,
    DatabaseOperationError
)


class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    def get_by_id(self, session: Session, category_id: int) -> Category:
        """Получить категорию по ID"""
        try:
            query = select(self._model).where(self._model.id == category_id)
            category = session.scalar(query)
            if not category:
                raise CategoryNotFoundException(
                    detail=f"Категория с ID {category_id} не найдена"
                )
            return category
        except SQLAlchemyError as e:
            raise DatabaseOperationError(
                detail=f"Ошибка при получении категории: {str(e)}"
            )

    def get_by_slug(self, session: Session, slug: str) -> Category | None:
        """Получить категорию по slug"""
        try:
            query = select(self._model).where(self._model.slug == slug)
            return session.scalar(query)
        except SQLAlchemyError as e:
            raise DatabaseOperationError(
                detail=f"Ошибка при получении категории по slug: {str(e)}"
            )

    def create(self, session: Session, category_data: CategoryCreate) -> Category:
        """Создать новую категорию"""
        try:
            query = (
                insert(self._model)
                .values(
                    title=category_data.title,
                    description=category_data.description,
                    slug=category_data.slug,
                    is_published=category_data.is_published,
                    created_at=datetime.now()
                )
                .returning(self._model)
            )
            category = session.scalar(query)
            session.flush()
            return category
        except IntegrityError:
            raise CategoryAlreadyExistsException(
                detail=f"Категория со slug '{category_data.slug}' уже существует"
            )
        except SQLAlchemyError as e:
            raise DatabaseOperationError(
                detail=f"Ошибка при создании категории: {str(e)}"
            )

    def update(self, session: Session, category_id: int, category_data: CategoryUpdate) -> Category:
        """Обновить категорию"""
        try:
            category = self.get_by_id(session, category_id)

            update_data = category_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(category, field):
                    setattr(category, field, value)

            session.flush()
            return category
        except IntegrityError:
            raise CategoryAlreadyExistsException(
                detail=f"Категория со slug '{category_data.slug}' уже существует"
            )
        except SQLAlchemyError as e:
            raise DatabaseOperationError(
                detail=f"Ошибка при обновлении категории: {str(e)}"
            )

    def delete(self, session: Session, category_id: int) -> None:
        """Удалить категорию по ID"""
        try:
            category = self.get_by_id(session, category_id)
            session.delete(category)
            session.flush()
        except SQLAlchemyError as e:
            raise DatabaseOperationError(
                detail=f"Ошибка при удалении категории: {str(e)}"
            )

    def get_by_title(self, session: Session, title: str) -> Category | None:
        """Получить категорию по названию"""
        try:
            query = select(self._model).where(self._model.title == title)
            return session.scalar(query)
        except SQLAlchemyError as e:
            raise DatabaseOperationError(
                detail=f"Ошибка при получении категории по названию: {str(e)}"
            )