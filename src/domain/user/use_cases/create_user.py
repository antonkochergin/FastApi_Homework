from core.exceptions.database_exceptions import AlreadyExistsException, NotFoundException
from core.exceptions.domain_exceptions import (
    UserWithEmailAlreadyExistException,
    UserWithUsernameAlreadyExistException,
)
from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import UserRepository
from resources.auth import get_password_hash
from schemas.user import UserCreate, UserResponse


class CreateUserUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, user_data: UserCreate) -> UserResponse:
        user_data.password = get_password_hash(password=user_data.password)

        async with self._database.session() as session:
            repo = UserRepository(session)

            try:
                new_user = await repo.create(user_data)
            except AlreadyExistsException:
                try:
                    await repo.get_by_username(user_data.username)
                    raise UserWithUsernameAlreadyExistException(user_data.username)
                except NotFoundException:
                    pass

                try:
                    await repo.get_by_email(user_data.email)
                    raise UserWithEmailAlreadyExistException(user_data.email)
                except NotFoundException:
                    pass

            return UserResponse.model_validate(new_user)
