from typing import List, Optional, Type

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.database_exceptions import NotFoundException
from infrastructure.postgres.models import Comment
from schemas.comment import CommentCreate, CommentUpdate


class CommentRepository:
    def __init__(self, session: AsyncSession):
        self._model: Type[Comment] = Comment
        self._session = session

    async def get(self, comment_id: int) -> Optional[Comment]:
        query = select(self._model).where(self._model.id == comment_id)

        comment = await self._session.scalar(query)
        if not comment:
            raise NotFoundException()

        return comment

    async def get_all(self) -> List[Comment]:
        result = await self._session.execute(select(self._model))
        return result.scalars().all()

    async def create(self, comment_data: CommentCreate, author_id: int) -> Comment:
        query = (
            insert(self._model)
            .values(**comment_data.model_dump(), user_id=author_id)
            .returning(self._model)
        )

        comment = await self._session.scalar(query)
        return comment

    async def update(self, comment_id: int, comment_data: CommentUpdate) -> Optional[Comment]:
        comment = await self.get(comment_id)

        update_data = comment_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(comment, key):
                setattr(comment, key, value)

        await self._session.commit()
        await self._session.refresh(comment)
        return comment

    async def delete(self, comment_id: int) -> bool:
        comment = await self.get(comment_id)

        await self._session.delete(comment)
        await self._session.commit()
        return True
