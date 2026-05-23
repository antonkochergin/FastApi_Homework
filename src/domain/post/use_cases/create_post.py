from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import CategoryNotFoundException, LocationNotFoundException
from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import (
    CategoryRepository,
    LocationRepository,
    PostRepository,
)
from schemas.post import PostCreate, PostResponse


class CreatePostUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, post_data: PostCreate, author_id: int) -> PostResponse:
        async with self._database.session() as session:
            repo = PostRepository(session)
            category_repo = CategoryRepository(session)
            location_repo = LocationRepository(session)

            try:
                await category_repo.get(post_data.category_id)
            except NotFoundException:
                raise CategoryNotFoundException(id=post_data.category_id)

            try:
                await location_repo.get(post_data.location_id)
            except NotFoundException:
                raise LocationNotFoundException(id=post_data.location_id)

            new_post = await repo.create(post_data, author_id)
            return PostResponse.model_validate(new_post)
