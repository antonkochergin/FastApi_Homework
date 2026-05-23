from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import PostNotFoundException
from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import CommentRepository, PostRepository
from schemas.comment import CommentCreate, CommentResponse


class CreateCommentUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, comment_data: CommentCreate, author_id: int) -> CommentResponse:
        async with self._database.session() as session:
            repo = CommentRepository(session)
            post_repo = PostRepository(session)

            try:
                await post_repo.get(comment_data.post_id)
            except NotFoundException:
                raise PostNotFoundException(id=comment_data.post_id)

            new_comment = await repo.create(comment_data, author_id)
            return CommentResponse.model_validate(new_comment)
