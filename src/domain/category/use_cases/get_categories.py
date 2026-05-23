from typing import List

from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import CategoryRepository
from schemas.category import CategoryResponse


class GetCategoriesUseCase:
    def __init__(self):
        self._database = database

    async def execute(self) -> List[CategoryResponse]:
        async with self._database.session() as session:
            repo = CategoryRepository(session)

            categorys = await repo.get_all()

            return [CategoryResponse.model_validate(category) for category in categorys]
