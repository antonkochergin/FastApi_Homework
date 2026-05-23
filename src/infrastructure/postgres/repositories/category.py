from typing import List, Optional, Type

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.database_exceptions import AlreadyExistsException, NotFoundException
from infrastructure.postgres.models import Category
from schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self._model: Type[Category] = Category
        self._session = session

    async def get(self, category_id: int) -> Optional[Category]:
        query = select(self._model).where(self._model.id == category_id)

        user = await self._session.scalar(query)
        if not user:
            raise NotFoundException()

        return user

    async def get_by_slug(self, slug: str) -> Optional[Category]:
        query = select(self._model).where(self._model.slug == slug)

        user = await self._session.scalar(query)
        if not user:
            raise NotFoundException()

        return user

    async def get_all(self) -> List[Category]:
        result = await self._session.execute(select(self._model))
        return result.scalars().all()

    async def create(self, category_data: CategoryCreate) -> Category:
        query = insert(self._model).values(category_data.model_dump()).returning(self._model)

        try:
            category = await self._session.scalar(query)
        except IntegrityError:
            raise AlreadyExistsException()

        return category

    async def update(self, category_id: int, category_data: CategoryUpdate) -> Optional[Category]:
        category = await self.get(category_id)

        update_data = category_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(category, key):
                setattr(category, key, value)

        await self._session.commit()
        await self._session.refresh(category)
        return category

    async def delete(self, category_id: int) -> bool:
        category = await self.get(category_id)

        await self._session.delete(category)
        await self._session.commit()
        return True
