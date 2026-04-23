from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.schemas.comments import Comment as CommentSchema
from src.core.exceptions.database_exceptions import CommentNotFoundException
from src.core.exceptions.domain_exceptions import CommentNotFoundByIdException


class GetCommentByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> CommentSchema:
        try:
            with self._database.session() as session:
                comment = self._repo.get_by_id(session=session, comment_id=comment_id)
        except CommentNotFoundException:
            raise CommentNotFoundByIdException(comment_id=comment_id)

        return CommentSchema.model_validate(obj=comment)