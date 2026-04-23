from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.schemas.locations import Location as LocationSchema, LocationUpdate
from src.core.exceptions.database_exceptions import (
    LocationNotFoundException,
    LocationAlreadyExistsException,
    DatabaseOperationError
)
from src.core.exceptions.domain_exceptions import (
    LocationNotFoundByIdException,
    LocationNameIsNotUniqueException,
    LocationNameEmptyException
)


class UpdateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int, location_data: LocationUpdate) -> LocationSchema:
        try:
            with self._database.session() as session:
                # Получаем существующую локацию
                try:
                    existing_location = self._repo.get_by_id(session, location_id)
                except LocationNotFoundException:
                    raise LocationNotFoundByIdException(location_id=location_id)

                # Проверяем название на пустоту
                if location_data.name is not None:
                    if not location_data.name or not location_data.name.strip():
                        raise LocationNameEmptyException()

                # Проверяем уникальность названия
                if location_data.name and location_data.name != existing_location.name:
                    same_name = self._repo.get_by_name(session, location_data.name)
                    if same_name:
                        raise LocationNameIsNotUniqueException(name=location_data.name)

                # Обновляем локацию
                location = self._repo.update(session, location_id, location_data)
        except LocationAlreadyExistsException:
            raise LocationNameIsNotUniqueException(name=location_data.name)

        return LocationSchema.model_validate(obj=location)