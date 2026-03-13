# fastapi_app/src/api/posts.py
from fastapi import APIRouter, status
from fastapi_app.src.schemas.posts import Post, PostCreate, PostUpdate
from fastapi_app.src.domain.posts_use_cases.create_post import CreatePostUseCase
from fastapi_app.src.domain.posts_use_cases.get_post import GetPostUseCase
from fastapi_app.src.domain.posts_use_cases.update_post import UpdatePostUseCase
from fastapi_app.src.domain.posts_use_cases.delete_post import DeletePostUseCase

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostCreate) -> Post:
    """Создать новый пост"""
    use_case = CreatePostUseCase()
    # ВРЕМЕННО: передаем фиксированный author_id = 1
    return await use_case.execute(
        author_id=1,  # заглушка, пока нет аутентификации
        post_data=post_data
    )


@router.get("/{post_id}", response_model=Post, status_code=status.HTTP_200_OK)
async def get_post(post_id: int) -> Post:
    """Получить пост по ID"""
    use_case = GetPostUseCase()
    return await use_case.execute(post_id=post_id)


@router.put("/{post_id}", response_model=Post, status_code=status.HTTP_200_OK)
async def update_post(post_id: int, post_data: PostUpdate) -> Post:
    """Обновить пост"""
    use_case = UpdatePostUseCase()
    # ВРЕМЕННО: передаем фиксированный user_id = 1
    return await use_case.execute(
        post_id=post_id,
        post_data=post_data,
        user_id=1,
        is_superuser=False
    )


@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int) -> dict:
    """Удалить пост"""
    use_case = DeletePostUseCase()
    # ВРЕМЕННО: передаем фиксированный user_id = 1
    return await use_case.execute(
        post_id=post_id,
        user_id=1,
        is_superuser=False
    )