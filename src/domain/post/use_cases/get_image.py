import os

from fastapi.responses import FileResponse

from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import PostHasNoImageException, PostNotFoundException
from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import PostRepository


class GetImageUseCase:
    def __init__(self):
        self._database = database
        self.image_folder = "../static/images"

    async def execute(self, post_id: int) -> FileResponse:
        async with self._database.session() as session:
            repo = PostRepository(session)

            try:
                post = await repo.get(post_id)
            except NotFoundException:
                raise PostNotFoundException(id=post_id)

            if not post.image:
                raise PostHasNoImageException(id=post_id)

            image_path = os.path.join(self.image_folder, post.image)

            if not os.path.exists(image_path):
                raise PostHasNoImageException()

            return FileResponse(image_path, media_type="image/jpeg")
