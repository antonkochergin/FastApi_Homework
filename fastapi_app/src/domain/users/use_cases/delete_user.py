from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users_repository import UsersRepository
from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import UserNotFoundByIdException


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UsersRepository()

    async def execute(self, user_id: int) -> dict:
        try:
            with self._database.session() as session:
                self._repo.delete(session=session, user_id=user_id)
        except UserNotFoundException:
            raise UserNotFoundByIdException(user_id=user_id)

        return {"message": f"Пользователь с ID {user_id} успешно удален"}