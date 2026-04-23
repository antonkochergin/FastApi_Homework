from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users_repository import UsersRepository
from src.schemas.users import User as UserSchema, UserCreate
from src.core.exceptions.database_exceptions import UserAlreadyExistsException
from src.core.exceptions.domain_exceptions import (
    UserUsernameIsNotUniqueException,
    UserEmailIsNotUniqueException
)
from src.resources.auth import get_password_hash  # <-- ДОБАВИТЬ ЭТУ СТРОКУ


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UsersRepository()

    async def execute(self, user_data: UserCreate) -> UserSchema:
        try:
            with self._database.session() as session:
                # Проверяем уникальность username
                existing_username = self._repo.get_by_username(session, user_data.username)
                if existing_username:
                    raise UserUsernameIsNotUniqueException(username=user_data.username)

                # Проверяем уникальность email
                if user_data.email:
                    existing_email = self._repo.get_by_email(session, user_data.email)
                    if existing_email:
                        raise UserEmailIsNotUniqueException(email=user_data.email)

                hashed_password = get_password_hash(user_data.password)
                user_data.password = hashed_password

                user = self._repo.create(session=session, user_data=user_data)
        except UserAlreadyExistsException:
            raise UserUsernameIsNotUniqueException(username=user_data.username)

        return UserSchema.model_validate(obj=user)