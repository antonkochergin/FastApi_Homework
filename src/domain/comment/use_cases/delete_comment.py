from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import (
    CommentNotFoundException,
    DomainPermissionDeniedException,
)
from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import CommentRepository
from schemas.user import UserResponse


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, comment_id: int, current_user: UserResponse) -> None:
        async with self._database.session() as session:
            repo = CommentRepository(session)

            try:
                comment = await repo.get(comment_id)
            except NotFoundException:
                raise CommentNotFoundException(id=comment_id)

            if not current_user.is_superuser and comment.user_id != current_user.id:
                raise DomainPermissionDeniedException(method="delete", model="comments")

            await repo.delete(comment_id)
