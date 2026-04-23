from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users_repository import UsersRepository
from src.schemas.users import User as UserSchema
from src.core.exceptions.domain_exceptions import UserNotFoundByUsernameException


class GetUserByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UsersRepository()

    async def execute(self, username: str) -> UserSchema:
        with self._database.session() as session:
            user = self._repo.get_by_username(session=session, username=username)
            if not user:
                raise UserNotFoundByUsernameException(username=username)

        return UserSchema.model_validate(obj=user)