from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import (
    CommentNotFoundException,
    DomainPermissionDeniedException,
)
from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import CommentRepository
from schemas.comment import CommentResponse, CommentUpdate
from schemas.user import UserResponse


class UpdateCommentUseCase:
    def __init__(self):
        self._database = database

    async def execute(
        self, comment_id: int, comment_data: CommentUpdate, current_user: UserResponse
    ) -> CommentResponse:
        async with self._database.session() as session:
            repo = CommentRepository(session)

            try:
                comment = await repo.get(comment_id)
            except NotFoundException:
                raise CommentNotFoundException(id=comment_id)

            if not current_user.is_superuser and comment.user_id != current_user.id:
                raise DomainPermissionDeniedException(method="update", model="comments")

            updated_comment = await repo.update(comment_id, comment_data)
            return CommentResponse.model_validate(updated_comment)
