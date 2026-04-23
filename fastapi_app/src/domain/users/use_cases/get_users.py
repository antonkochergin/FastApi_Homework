from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users_repository import UsersRepository
from src.schemas.users import User as UserSchema


class GetUsersUseCase:
    def __init__(self):
        self._database = database
        self._repo = UsersRepository()

    async def execute(self) -> list[UserSchema]:
        with self._database.session() as session:
            users = self._repo.get_all(session=session)

        return [UserSchema.model_validate(obj=user) for user in users]