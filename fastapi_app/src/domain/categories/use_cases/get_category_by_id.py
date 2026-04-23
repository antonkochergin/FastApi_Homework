from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category_repository import CategoryRepository
from src.schemas.categories import Category as CategorySchema
from src.core.exceptions.database_exceptions import CategoryNotFoundException
from src.core.exceptions.domain_exceptions import CategoryNotFoundByIdException


class GetCategoryByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> CategorySchema:
        try:
            with self._database.session() as session:
                category = self._repo.get_by_id(session, category_id)
        except CategoryNotFoundException:
            raise CategoryNotFoundByIdException(category_id=category_id)

        return CategorySchema.model_validate(obj=category)