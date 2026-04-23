from typing import Type, Optional
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime

from src.infrastructure.sqlite.models.post import Post
from src.schemas.posts import PostCreate, PostUpdate
from src.core.exceptions.database_exceptions import (
    PostNotFoundException,
    PostAuthorNotFoundExceptionDB,
    PostCategoryNotFoundExceptionDB,
    PostLocationNotFoundExceptionDB,
    DatabaseOperationError
)


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post

    def get_by_id(self, session: Session, post_id: int) -> Post:
        """Получить пост по ID"""
        try:
            query = select(self._model).where(self._model.id == post_id)
            post = session.scalar(query)
            if not post:
                raise PostNotFoundException(
                    detail=f"Пост с ID {post_id} не найден"
                )
            return post
        except SQLAlchemyError as e:
            raise DatabaseOperationError(
                detail=f"Ошибка при получении поста: {str(e)}"
            )

    def create(self, session: Session, post_data: PostCreate) -> Post:
        """Создать новый пост"""
        try:
            query = (
                insert(self._model)
                .values(
                    title=post_data.title,
                    text=post_data.text,
                    pub_date=post_data.pub_date,
                    author_id=post_data.author_id,
                    category_id=post_data.category_id,
                    location_id=post_data.location_id,
                    image=post_data.image,
                    is_published=post_data.is_published,
                    created_at=datetime.now()
                )
                .returning(self._model)
            )
            post = session.scalar(query)
            session.flush()
            return post
        except IntegrityError as e:
            if "FOREIGN KEY" in str(e):
                if "author_id" in str(e):
                    raise PostAuthorNotFoundExceptionDB(
                        detail=f"Автор с ID {post_data.author_id} не найден"
                    )
                elif "category_id" in str(e):
                    raise PostCategoryNotFoundExceptionDB(
                        detail=f"Категория с ID {post_data.category_id} не найдена"
                    )
                elif "location_id" in str(e):
                    raise PostLocationNotFoundExceptionDB(
                        detail=f"Локация с ID {post_data.location_id} не найдена"
                    )
            raise DatabaseOperationError(
                detail=f"Ошибка целостности данных: {str(e)}"
            )
        except SQLAlchemyError as e:
            raise DatabaseOperationError(
                detail=f"Ошибка при создании поста: {str(e)}"
            )

    def update(self, session: Session, post_id: int, post_data: PostUpdate) -> Post:
        """Обновить пост"""
        try:
            post = self.get_by_id(session, post_id)

            update_data = post_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(post, field):
                    setattr(post, field, value)

            session.flush()
            return post
        except IntegrityError as e:
            if "FOREIGN KEY" in str(e):
                if "author_id" in str(e):
                    raise PostAuthorNotFoundExceptionDB(
                        detail=f"Автор с ID {post_data.author_id} не найден"
                    )
                elif "category_id" in str(e):
                    raise PostCategoryNotFoundExceptionDB(
                        detail=f"Категория с ID {post_data.category_id} не найдена"
                    )
                elif "location_id" in str(e):
                    raise PostLocationNotFoundExceptionDB(
                        detail=f"Локация с ID {post_data.location_id} не найдена"
                    )
            raise DatabaseOperationError(
                detail=f"Ошибка целостности данных: {str(e)}"
            )
        except SQLAlchemyError as e:
            raise DatabaseOperationError(
                detail=f"Ошибка при обновлении поста: {str(e)}"
            )

    def delete(self, session: Session, post_id: int) -> None:
        """Удалить пост"""
        try:
            post = self.get_by_id(session, post_id)
            session.delete(post)
            session.flush()
        except SQLAlchemyError as e:
            raise DatabaseOperationError(
                detail=f"Ошибка при удалении поста: {str(e)}"
            )