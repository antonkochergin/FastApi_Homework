from typing import List, Optional, Type

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.database_exceptions import AlreadyExistsException, NotFoundException
from infrastructure.postgres.models import Location
from schemas.location import LocationCreate


class LocationRepository:
    def __init__(self, session: AsyncSession):
        self._model: Type[Location] = Location
        self._session = session

    async def get(self, location_id: int) -> Optional[Location]:
        query = select(self._model).where(self._model.id == location_id)

        location = await self._session.scalar(query)
        if not location:
            raise NotFoundException()

        return location

    async def get_by_name(self, name: str) -> Optional[Location]:
        query = select(self._model).where(self._model.name == name)

        location = await self._session.scalar(query)
        if not location:
            raise NotFoundException()

        return location

    async def get_all(self) -> List[Location]:
        result = await self._session.execute(select(self._model))
        return result.scalars().all()

    async def create(self, location_data: LocationCreate) -> Location:
        query = insert(self._model).values(location_data.model_dump()).returning(self._model)

        try:
            location = await self._session.scalar(query)
        except IntegrityError:
            raise AlreadyExistsException()

        return location

    async def delete(self, location_id: int) -> bool:
        location = await self.get(location_id)

        await self._session.delete(location)
        await self._session.commit()
        return True
