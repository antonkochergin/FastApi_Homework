from typing import Type
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from src.infrastructure.sqlite.models.comment import Comment
from src.schemas.comments import CommentCreate, CommentUpdate
from src.core.exceptions.database_exceptions import (
    CommentNotFoundException,
    CommentAuthorNotFoundExceptionDB,
    CommentPostNotFoundExceptionDB,
    CommentIntegrityError
)


class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment

    def get_by_id(self, session: Session, comment_id: int) -> Comment:
        query = (
            select(self._model)
            .where(self._model.id == comment_id)
        )
        comment = session.scalar(query)
        if not comment:
            raise CommentNotFoundException()
        return comment

    def create(self, session: Session, comment_data: CommentCreate) -> Comment:
        query = (
            insert(self._model)
            .values(
                text=comment_data.text,
                post_id=comment_data.post_id,
                author_id=comment_data.author_id,
                created_at=datetime.now()
            )
            .returning(self._model)
        )
        try:
            comment = session.scalar(query)
            session.flush()
            return comment
        except IntegrityError as e:
            if "FOREIGN KEY" in str(e):
                if "author_id" in str(e):
                    raise CommentAuthorNotFoundExceptionDB()
                elif "post_id" in str(e):
                    raise CommentPostNotFoundExceptionDB()
            raise CommentIntegrityError()

    def update(self, session: Session, comment_id: int, comment_data: CommentUpdate) -> Comment:
        comment = self.get_by_id(session, comment_id)
        comment.text = comment_data.text
        session.flush()
        return comment

    def delete(self, session: Session, comment_id: int) -> None:
        comment = self.get_by_id(session, comment_id)
        session.delete(comment)
        session.flush()