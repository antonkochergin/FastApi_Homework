from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users_repository import UsersRepository
from src.schemas.users import User as UserSchema
from src.core.exceptions.domain_exceptions import UserNotFoundByLoginException


class GetUserByLoginUseCase:
    def __init__(self):
        self._database = database
        self._repo = UsersRepository()

    async def execute(self, login: str) -> UserSchema:
        with self._database.session() as session:
            user = self._repo.get_by_username(session=session, username=login)
            if not user:
                raise UserNotFoundByLoginException(login=login)

        return UserSchema.model_validate(obj=user)