from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import CategoryNotFoundBySlugException
from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import CategoryRepository
from schemas.category import CategoryResponse


class GetCategoryBySlugUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, slug: str) -> CategoryResponse:
        async with self._database.session() as session:
            repo = CategoryRepository(session)

            try:
                category = await repo.get_by_slug(slug)
            except NotFoundException:
                raise CategoryNotFoundBySlugException(slug=slug)

            return CategoryResponse.model_validate(category)
