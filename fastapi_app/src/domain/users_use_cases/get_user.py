from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.users_repo import UserRepository
from fastapi_app.src.schemas.users import User


class GetUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> User:
        """Получить пользователя по ID"""

        with self._database.session() as session:
            user = self._repo.get_by_id(session, user_id)
        return User.model_validate(user)

