from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import (
    CategoryNotFoundException,
    CategoryWithSlugAlreadyExistException,
    NotEnoughRightsException,
)
from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import CategoryRepository
from schemas.category import CategoryResponse, CategoryUpdate
from schemas.user import UserResponse


class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database

    async def execute(
        self, category_id: int, category_data: CategoryUpdate, current_user: UserResponse
    ) -> CategoryResponse:
        async with self._database.session() as session:
            repo = CategoryRepository(session)

            if not current_user.is_superuser:
                raise NotEnoughRightsException(current_user.username)

            try:
                category = await repo.get(category_id)
            except NotFoundException:
                raise CategoryNotFoundException(id=category_id)

            if category_data.slug:
                try:
                    category_with_slug = await repo.get_by_slug(category_data.slug)
                    if category_with_slug.id != category.id:
                        raise CategoryWithSlugAlreadyExistException(category_data.slug)
                except NotFoundException:
                    pass

            updated_category = await repo.update(category_id, category_data)
            return CategoryResponse.model_validate(updated_category)
