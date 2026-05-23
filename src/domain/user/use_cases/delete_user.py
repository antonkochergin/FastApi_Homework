from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import (
    DomainPermissionDeniedException,
    UserNotFoundException,
)
from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import UserRepository
from schemas.user import UserResponse


class DeleteUserUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, user_id: int, current_user: UserResponse) -> None:
        async with self._database.session() as session:
            repo = UserRepository(session)

            try:
                await repo.get(user_id)
            except NotFoundException:
                raise UserNotFoundException(id=user_id)

            if not current_user.is_superuser and user_id != current_user.id:
                raise DomainPermissionDeniedException(method="delete", model="users")

            await repo.delete(user_id)
