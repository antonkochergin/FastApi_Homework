from typing import List

from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import CommentRepository
from schemas.comment import CommentResponse


class GetCommentsUseCase:
    def __init__(self):
        self._database = database

    async def execute(self) -> List[CommentResponse]:
        async with self._database.session() as session:
            repo = CommentRepository(session)

            comments = await repo.get_all()

            return [CommentResponse.model_validate(comment) for comment in comments]
