from typing import List

from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import PostRepository
from schemas.post import PostResponse


class GetPostsUseCase:
    def __init__(self):
        self._database = database

    async def execute(self) -> List[PostResponse]:
        async with self._database.session() as session:
            repo = PostRepository(session)

            posts = await repo.get_all()

            return [PostResponse.model_validate(post) for post in posts]
