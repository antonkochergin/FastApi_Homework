from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import LocationNotFoundException
from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import LocationRepository
from schemas.location import LocationResponse


class GetLocationUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, location_id: int) -> LocationResponse:
        async with self._database.session() as session:
            repo = LocationRepository(session)

            try:
                location = await repo.get(location_id)
            except NotFoundException:
                raise LocationNotFoundException(location_id)

            return LocationResponse.model_validate(location)
