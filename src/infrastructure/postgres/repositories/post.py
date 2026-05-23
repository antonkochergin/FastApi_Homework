from typing import List, Optional, Type

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.database_exceptions import NotFoundException
from infrastructure.postgres.models import Post
from schemas.post import PostCreate, PostUpdate


class PostRepository:
    def __init__(self, session: AsyncSession):
        self._model: Type[Post] = Post
        self._session = session

    async def get(self, post_id: int) -> Optional[Post]:
        query = select(self._model).where(self._model.id == post_id)

        post = await self._session.scalar(query)
        if not post:
            raise NotFoundException()

        return post

    async def get_all(self) -> List[Post]:
        result = await self._session.execute(select(self._model))
        return result.scalars().all()

    async def create(self, post_data: PostCreate, author_id: int) -> Post:
        query = (
            insert(self._model)
            .values(**post_data.model_dump(), user_id=author_id)
            .returning(self._model)
        )

        post = await self._session.scalar(query)
        return post

    async def update(self, post_id: int, post_data: PostUpdate) -> Optional[Post]:
        post = await self.get(post_id)

        update_data = post_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(post, key):
                setattr(post, key, value)

        await self._session.commit()
        await self._session.refresh(post)
        return post

    async def delete(self, post_id: int) -> bool:
        post = await self.get(post_id)

        await self._session.delete(post)
        await self._session.commit()
        return True
