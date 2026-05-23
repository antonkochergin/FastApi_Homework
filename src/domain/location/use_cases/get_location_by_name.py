from core.exceptions.domain_exceptions import LocationNotFoundByNameException
from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import LocationRepository
from schemas.location import LocationResponse


class GetLocationBySlugUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, name: str) -> LocationResponse:
        async with self._database.session() as session:
            repo = LocationRepository(session)

            try:
                location = await repo.get_by_name(name)
            except:
                raise LocationNotFoundByNameException(name=name)

            return LocationResponse.model_validate(location)
