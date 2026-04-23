from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category_repository import CategoryRepository
from src.core.exceptions.database_exceptions import CategoryNotFoundException
from src.core.exceptions.domain_exceptions import CategoryNotFoundByIdException


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> dict:
        try:
            with self._database.session() as session:
                self._repo.delete(session, category_id)
        except CategoryNotFoundException:
            raise CategoryNotFoundByIdException(category_id=category_id)

        return {"message": f"Категория с ID {category_id} успешно удалена"}