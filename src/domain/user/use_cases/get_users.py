from typing import List

from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import UserRepository
from schemas.user import UserResponse


class GetUsersUseCase:
    def __init__(self):
        self._database = database

    async def execute(self) -> List[UserResponse]:
        async with self._database.session() as session:
            repo = UserRepository(session)

            users = await repo.get_all()

            return [UserResponse.model_validate(user) for user in users]
