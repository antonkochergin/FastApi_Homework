from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.users_repo import UserRepository
from fastapi_app.src.schemas.users import UserCreate, User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_data: UserCreate) -> User:
        """Создать нового пользователя"""
        with self._database.session() as session:
                # Проверка уникальности username
            existing_username = self._repo.get_by_username(session, user_data.username)

                # Проверка уникальности email (если указан)
            if user_data.email:
                existing_email = session.query(self._repo.model).filter(
                    self._repo.model.email == user_data.email
                ).first()

                # Хешируем пароль
            hashed_password = pwd_context.hash(user_data.password)

                # Создаем пользователя
            new_user = self._repo.create(session, user_data, hashed_password)
            return User.model_validate(new_user)