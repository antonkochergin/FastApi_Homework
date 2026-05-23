from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import CommentNotFoundException
from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import CommentRepository
from schemas.comment import CommentResponse


class GetCommentUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, comment_id: int) -> CommentResponse:
        async with self._database.session() as session:
            repo = CommentRepository(session)

            try:
                comment = await repo.get(comment_id)
            except NotFoundException:
                raise CommentNotFoundException(id=comment_id)

            return CommentResponse.model_validate(comment)
