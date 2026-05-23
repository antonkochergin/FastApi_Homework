from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import UserNotFoundByUsernameException
from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import UserRepository
from schemas.user import UserResponse


class GetUserByUsernameUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, username: str) -> UserResponse:
        async with self._database.session() as session:
            repo = UserRepository(session)

            try:
                user = await repo.get_by_username(username)
            except NotFoundException:
                UserNotFoundByUsernameException(username=username)

            return UserResponse.model_validate(user)
