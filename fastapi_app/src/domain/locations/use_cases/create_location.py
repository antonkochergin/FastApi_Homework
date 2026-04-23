from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.schemas.locations import Location as LocationSchema, LocationCreate
from src.core.exceptions.database_exceptions import (
    LocationAlreadyExistsException,
    DatabaseOperationError
)
from src.core.exceptions.domain_exceptions import (
    LocationNameIsNotUniqueException,
    LocationNameEmptyException
)


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_data: LocationCreate) -> LocationSchema:
        # Проверка на пустое название
        if not location_data.name or not location_data.name.strip():
            raise LocationNameEmptyException()

        try:
            with self._database.session() as session:
                # Проверяем уникальность названия
                existing = self._repo.get_by_name(session, location_data.name)
                if existing:
                    raise LocationNameIsNotUniqueException(name=location_data.name)

                location = self._repo.create(session, location_data)
        except LocationAlreadyExistsException:
            raise LocationNameIsNotUniqueException(name=location_data.name)
        except DatabaseOperationError:
            raise

        return LocationSchema.model_validate(obj=location)