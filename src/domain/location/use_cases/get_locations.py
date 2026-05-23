from typing import List

from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import LocationRepository
from schemas.location import LocationResponse


class GetLocationsUseCase:
    def __init__(self):
        self._database = database

    async def execute(self) -> List[LocationResponse]:
        async with self._database.session() as session:
            repo = LocationRepository(session)

            locations = await repo.get_all()

            return [LocationResponse.model_validate(location) for location in locations]
