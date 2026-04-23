from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.core.exceptions.database_exceptions import CommentNotFoundException
from src.core.exceptions.domain_exceptions import CommentNotFoundByIdException


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> dict:
        try:
            with self._database.session() as session:
                self._repo.delete(session=session, comment_id=comment_id)
        except CommentNotFoundException:
            raise CommentNotFoundByIdException(comment_id=comment_id)

        return {"message": f"Комментарий с ID {comment_id} успешно удален"}