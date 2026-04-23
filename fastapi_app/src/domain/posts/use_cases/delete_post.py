from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.core.exceptions.database_exceptions import PostNotFoundException
from src.core.exceptions.domain_exceptions import PostNotFoundByIdException


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> dict:
        try:
            with self._database.session() as session:
                self._repo.delete(session, post_id)
        except PostNotFoundException:
            raise PostNotFoundByIdException(post_id=post_id)

        return {"message": f"Пост с ID {post_id} успешно удален"}