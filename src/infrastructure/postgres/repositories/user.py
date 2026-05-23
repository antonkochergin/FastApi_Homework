from typing import List, Optional, Type

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.database_exceptions import AlreadyExistsException, NotFoundException
from infrastructure.postgres.models import User
from schemas.user import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._model: Type[User] = User
        self._session = session

    async def get(self, user_id: int) -> Optional[User]:
        query = select(self._model).where(self._model.id == user_id)

        user = await self._session.scalar(query)
        if not user:
            raise NotFoundException()

        return user

    async def get_by_username(self, username: str) -> Optional[User]:
        query = select(self._model).where(self._model.username == username)

        user = await self._session.scalar(query)
        if not user:
            raise NotFoundException()

        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(self._model).where(self._model.email == email)

        user = await self._session.scalar(query)
        if not user:
            raise NotFoundException()

        return user

    async def get_all(self) -> List[User]:
        result = await self._session.execute(select(self._model))
        return result.scalars().all()

    async def create(self, user_data: UserCreate) -> User:
        data = user_data.model_dump()

        query = insert(self._model).values(data).returning(self._model)

        try:
            user = await self._session.scalar(query)
        except IntegrityError:
            raise AlreadyExistsException()

        return user

    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        user = await self.get(user_id)

        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        user = await self.get(user_id)

        await self._session.delete(user)
        await self._session.commit()
        return True
