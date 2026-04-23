from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users_repository import UsersRepository
from src.schemas.users import User as UserSchema, UserUpdate
from src.core.exceptions.database_exceptions import UserNotFoundException, UserAlreadyExistsException
from src.core.exceptions.domain_exceptions import (
    UserNotFoundByIdException,
    UserUsernameIsNotUniqueException,
    UserEmailIsNotUniqueException
)


class UpdateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UsersRepository()

    async def execute(self, user_id: int, user_data: UserUpdate) -> UserSchema:
        try:
            with self._database.session() as session:
                # Получаем существующего пользователя
                try:
                    existing_user = self._repo.get_by_id(session, user_id)
                except UserNotFoundException:
                    raise UserNotFoundByIdException(user_id=user_id)

                # Проверяем уникальность username
                if user_data.username and user_data.username != existing_user.username:
                    same_username = self._repo.get_by_username(session, user_data.username)
                    if same_username:
                        raise UserUsernameIsNotUniqueException(username=user_data.username)

                # Проверяем уникальность email
                if user_data.email and user_data.email != existing_user.email:
                    same_email = self._repo.get_by_email(session, user_data.email)
                    if same_email:
                        raise UserEmailIsNotUniqueException(email=user_data.email)

                # Обновляем пользователя
                user = self._repo.update(session, user_id, user_data)
        except UserAlreadyExistsException:
            raise UserUsernameIsNotUniqueException(username=user_data.username)

        return UserSchema.model_validate(obj=user)