from core.exceptions.database_exceptions import AlreadyExistsException
from core.exceptions.domain_exceptions import (
    LocationWithNameAlreadyExistException,
    NotEnoughRightsException,
)
from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import LocationRepository
from schemas.location import LocationCreate, LocationResponse
from schemas.user import UserResponse


class CreateLocationUseCase:
    def __init__(self):
        self._database = database

    async def execute(
        self, location_data: LocationCreate, current_user: UserResponse
    ) -> LocationResponse:
        async with self._database.session() as session:
            repo = LocationRepository(session)

            if not current_user.is_superuser:
                raise NotEnoughRightsException(current_user.username)

            try:
                new_location = await repo.create(location_data)
            except AlreadyExistsException:
                raise LocationWithNameAlreadyExistException(location_data.name)

            return LocationResponse.model_validate(new_location)
