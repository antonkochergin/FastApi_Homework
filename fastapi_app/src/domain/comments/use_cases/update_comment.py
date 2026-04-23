from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.schemas.comments import Comment as CommentSchema, CommentUpdate
from src.core.exceptions.database_exceptions import CommentNotFoundException
from src.core.exceptions.domain_exceptions import CommentNotFoundByIdException


class UpdateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int, comment_data: CommentUpdate) -> CommentSchema:
        try:
            with self._database.session() as session:
                comment = self._repo.update(
                    session=session,
                    comment_id=comment_id,
                    comment_data=comment_data
                )
        except CommentNotFoundException:
            raise CommentNotFoundByIdException(comment_id=comment_id)

        return CommentSchema.model_validate(obj=comment)