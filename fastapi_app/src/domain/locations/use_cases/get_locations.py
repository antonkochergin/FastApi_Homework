from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.schemas.locations import Location as LocationSchema
from src.core.exceptions.database_exceptions import DatabaseOperationError


class GetLocationsUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, published_only: bool = False) -> list[LocationSchema]:
        try:
            with self._database.session() as session:
                if published_only:
                    locations = self._repo.get_published(session)
                else:
                    locations = self._repo.get_all(session)

                return [LocationSchema.model_validate(loc) for loc in locations]
        except DatabaseOperationError:
            raise
        except Exception as e:
            raise DatabaseOperationError(
                detail=f"Неожиданная ошибка при получении локаций: {str(e)}"
            )