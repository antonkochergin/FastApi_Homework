from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import (
    DomainPermissionDeniedException,
    UserNotFoundException,
    UserWithEmailAlreadyExistException,
    UserWithUsernameAlreadyExistException,
)
from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import UserRepository
from schemas.user import UserResponse, UserUpdate


class UpdateUserUseCase:
    def __init__(self):
        self._database = database

    async def execute(
        self, user_id: int, user_data: UserUpdate, current_user: UserResponse
    ) -> UserResponse:
        async with self._database.session() as session:
            repo = UserRepository(session)

            try:
                await repo.get(user_id)
            except NotFoundException:
                raise UserNotFoundException(user_id)

            if not current_user.is_superuser and user_id != current_user.id:
                raise DomainPermissionDeniedException(method="update", model="users")

            if user_data.username:
                try:
                    user_with_username = await repo.get_by_username(user_data.username)
                    if user_with_username and user_with_username.id != user_id:
                        raise UserWithUsernameAlreadyExistException(user_data.username)
                except NotFoundException:
                    pass

            if user_data.email:
                try:
                    user_with_email = await repo.get_by_email(user_data.email)
                    if user_with_email and user_with_email.id != user_id:
                        raise UserWithEmailAlreadyExistException(user_data.email)
                except NotFoundException:
                    pass

            updated_user = await repo.update(user_id, user_data)
            return UserResponse.model_validate(updated_user)
