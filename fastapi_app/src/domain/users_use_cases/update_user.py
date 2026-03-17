from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.users_repo import UserRepository
from fastapi_app.src.schemas.users import UserUpdate, User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UpdateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, user_data: UserUpdate) -> User:
        """Обновить данные пользователя"""
        with self._database.session() as session:
                # Проверяем, существует ли пользователь
            existing_user = self._repo.get_by_id(session, user_id)

                # Если обновляется username, проверяем уникальность
            if user_data.username and user_data.username != existing_user.username:
                same_username = self._repo.get_by_username(session, user_data.username)

                # Если обновляется email, проверяем уникальность
            if user_data.email and user_data.email != existing_user.email:
                same_email = session.query(self._repo.model).filter(
                    self._repo.model.email == user_data.email
                ).first()


                # Если обновляется пароль - хешируем
            if user_data.password:
                user_data.password = pwd_context.hash(user_data.password)

                # Обновляем пользователя
            updated_user = self._repo.update(session, user_id, user_data)


        return User.model_validate(updated_user)
