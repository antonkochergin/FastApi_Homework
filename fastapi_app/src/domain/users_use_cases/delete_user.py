from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.users_repo import UserRepository


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> dict:
        """Удалить пользователя"""
        with self._database.session() as session:
                # Проверяем, существует ли пользователь
            deleted = self._repo.delete(session, user_id)

            return {"message": f"Пользователь с ID {user_id} успешно удален"}