from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.schemas.locations import Location as LocationSchema
from src.core.exceptions.database_exceptions import LocationNotFoundException
from src.core.exceptions.domain_exceptions import LocationNotFoundByIdException


class GetLocationByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> LocationSchema:
        try:
            with self._database.session() as session:
                location = self._repo.get_by_id(session, location_id)
        except LocationNotFoundException:
            raise LocationNotFoundByIdException(location_id=location_id)

        return LocationSchema.model_validate(obj=location)