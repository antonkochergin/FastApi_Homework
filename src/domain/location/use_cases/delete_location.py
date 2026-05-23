from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import LocationNotFoundException, NotEnoughRightsException
from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import LocationRepository
from schemas.user import UserResponse


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, location_id: int, current_user: UserResponse) -> None:
        async with self._database.session() as session:
            repo = LocationRepository(session)

            if not current_user.is_superuser:
                raise NotEnoughRightsException(current_user.username)

            try:
                await repo.delete(location_id)
            except NotFoundException:
                raise LocationNotFoundException(id=location_id)
