from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import (
    CategoryNotFoundException,
    DomainPermissionDeniedException,
    LocationNotFoundException,
    PostNotFoundException,
)
from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import (
    CategoryRepository,
    LocationRepository,
    PostRepository,
)
from schemas.post import PostResponse, PostUpdate
from schemas.user import UserResponse


class UpdatePostUseCase:
    def __init__(self):
        self._database = database

    async def execute(
        self, post_id: int, post_data: PostUpdate, current_user: UserResponse
    ) -> PostResponse:
        async with self._database.session() as session:
            repo = PostRepository(session)
            category_repo = CategoryRepository(session)
            location_repo = LocationRepository(session)

            try:
                existing_post = await repo.get(post_id)
            except NotFoundException:
                raise PostNotFoundException(id=post_id)

            if not current_user.is_superuser and existing_post.user_id != current_user.id:
                raise DomainPermissionDeniedException(method="update", model="posts")

            if post_data.category_id and post_data.category_id != existing_post.category_id:
                try:
                    await category_repo.get(post_data.category_id)
                except NotFoundException:
                    raise CategoryNotFoundException(id=post_data.category_id)

            if post_data.location_id and post_data.location_id != existing_post.location_id:
                try:
                    await location_repo.get(post_data.location_id)
                except NotFoundException:
                    raise LocationNotFoundException(id=post_data.location_id)

            updated_post = await repo.update(post_id, post_data)
            return PostResponse.model_validate(updated_post)
