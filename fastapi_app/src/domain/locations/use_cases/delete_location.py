from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.core.exceptions.database_exceptions import LocationNotFoundException
from src.core.exceptions.domain_exceptions import LocationNotFoundByIdException


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> dict:
        try:
            with self._database.session() as session:
                self._repo.delete(session, location_id)
        except LocationNotFoundException:
            raise LocationNotFoundByIdException(location_id=location_id)

        return {"message": f"Локация с ID {location_id} успешно удалена"}