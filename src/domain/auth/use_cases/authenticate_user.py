from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import (
    InvalidPasswordException,
    UserNotFoundByUsernameException,
)
from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import UserRepository
from resources.auth import verify_password
from schemas.user import UserResponse


class AuthenticateUserUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, username: str, password: str) -> UserResponse:
        async with self._database.session() as session:
            try:
                repo = UserRepository(session)
                user = await repo.get_by_username(username=username)
            except NotFoundException:
                raise UserNotFoundByUsernameException(username)

            if not verify_password(plain_password=password, hashed_password=user.password):
                raise InvalidPasswordException

            return UserResponse.model_validate(obj=user)
