from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import PostNotFoundException
from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import PostRepository
from schemas.post import PostResponse


class GetPostUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, post_id: int) -> PostResponse:
        async with self._database.session() as session:
            repo = PostRepository(session)

            try:
                post = await repo.get(post_id)
            except NotFoundException:
                raise PostNotFoundException(id=post_id)

            return PostResponse.model_validate(post)
