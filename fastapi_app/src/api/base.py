from fastapi import APIRouter, status, HTTPException
from ..schemas.posts import Post

# Временное хранилище постов
posts_db = []
post_counter = 1

router = APIRouter()


@router.get("/hello_world", status_code=status.HTTP_200_OK)
async def get_hello_world() -> dict:
    response = {"text": "Hello, World!"}

    return response


@router.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post) -> dict:
    global post_counter

    if len(post.text) < 10:
        raise HTTPException(
            detail="Длина поста должна быть не меньше 10 символов",
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        )

    # Добавляем ID к посту и сохраняем
    post_dict = post.model_dump()
    post_dict["id"] = post_counter
    post_counter += 1
    posts_db.append(post_dict)

    response = {
        "title": post.title,
        "text": post.text,
        "author_id": post.author_id,
        "pub_date": post.pub_date,
        "location_id": post.location_id,
        "category_id": post.category_id,
        "id": post_dict["id"]
    }

    return response


@router.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def get_post(post_id: int) -> dict:
    """Получение конкретного поста по ID"""
    # Ищем пост во временном хранилище
    for post in posts_db:
        if post["id"] == post_id:
            return post

    # Если пост не найден
    raise HTTPException(
        detail=f"Пост с id {post_id} не найден",
        status_code=status.HTTP_404_NOT_FOUND,
    )


@router.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def update_post(post_id: int, updated_post: Post) -> dict:
    """Полное обновление поста"""
    # Ищем пост
    for i, post in enumerate(posts_db):
        if post["id"] == post_id:
            # Валидация текста
            if len(updated_post.text) < 10:
                raise HTTPException(
                    detail="Длина поста должна быть не меньше 10 символов",
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                )

            # Обновляем все поля
            updated_data = updated_post.model_dump()
            updated_data["id"] = post_id  # сохраняем тот же ID
            posts_db[i] = updated_data

            return updated_data

    raise HTTPException(
        detail=f"Пост с id {post_id} не найден",
        status_code=status.HTTP_404_NOT_FOUND,
    )


@router.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int) -> dict:
    """Удаление поста по ID"""
    # Ищем пост
    for i, post in enumerate(posts_db):
        if post["id"] == post_id:
            # Удаляем пост из хранилища
            deleted_post = posts_db.pop(i)

            return {
                "message": "Пост успешно удален",
                "deleted_post": deleted_post
            }

    raise HTTPException(
        detail=f"Пост с id {post_id} не найден",
        status_code=status.HTTP_404_NOT_FOUND,
    )