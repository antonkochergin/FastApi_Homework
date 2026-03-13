from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.posts_repo import PostRepository
from fastapi_app.src.schemas.posts import PostCreate, Post
from fastapi_app.src.infrastructure.sqlite.models.categories import Category
from fastapi_app.src.infrastructure.sqlite.models.locations import Location
import logging

logger = logging.getLogger(__name__)

class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, author_id: int, post_data: PostCreate) -> Post:
        try:
            with self._database.session() as session:
                # Проверка author_id
                if not author_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="ID автора обязателен"
                    )

                # Проверка существования категории
                if post_data.category_id is not None:
                    category = session.get(Category, post_data.category_id)
                    if not category:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Категория с ID {post_data.category_id} не найдена"
                        )

                # Проверка существования локации
                if post_data.location_id is not None:
                    location = session.get(Location, post_data.location_id)
                    if not location:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Локация с ID {post_data.location_id} не найдена"
                        )

                new_post = self._repo.create(session, post_data, author_id)

                if not new_post:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось создать пост"
                    )

                return Post.model_validate(new_post)

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Ошибка при создании поста: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )