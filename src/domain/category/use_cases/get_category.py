from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import CategoryNotFoundException
from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import CategoryRepository
from schemas.category import CategoryResponse


class GetCategoryUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, category_id: int) -> CategoryResponse:
        async with self._database.session() as session:
            repo = CategoryRepository(session)

            try:
                category = await repo.get(category_id)
            except NotFoundException:
                raise CategoryNotFoundException(id=category_id)

            return CategoryResponse.model_validate(category)
