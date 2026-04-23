from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import ValidationError
from src.schemas.posts import Post, PostCreate, PostUpdate
from src.domain.posts.use_cases.get_post_by_id import GetPostByIdUseCase
from src.domain.posts.use_cases.create_post import CreatePostUseCase
from src.domain.posts.use_cases.update_post import UpdatePostUseCase
from src.domain.posts.use_cases.delete_post import DeletePostUseCase
from src.core.exceptions.database_exceptions import DatabaseOperationError
from src.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    PostAuthorNotFoundException,
    PostCategoryNotFoundException,
    PostLocationNotFoundException,
    PostTitleEmptyException,
    PostTextEmptyException
)

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/{post_id}", response_model=Post, status_code=status.HTTP_200_OK)
async def get_post_by_id(
    post_id: int,
    use_case: GetPostByIdUseCase = Depends()
) -> Post:
    """Получить пост по ID"""
    try:
        return await use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.get_detail()
        )
    except DatabaseOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e._detail or "Внутренняя ошибка сервера"
        )


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    use_case: CreatePostUseCase = Depends()
) -> Post:
    """Создать новый пост"""
    try:
        return await use_case.execute(post_data=post_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )
    except PostTitleEmptyException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.get_detail()
        )
    except PostTextEmptyException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.get_detail()
        )
    except PostAuthorNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # 404, а не 400
            detail=e.get_detail()
        )
    except PostCategoryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # 404, а не 400
            detail=e.get_detail()
        )
    except PostLocationNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # 404, а не 400
            detail=e.get_detail()
        )
    except DatabaseOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e._detail or "Внутренняя ошибка сервера"
        )


@router.put("/{post_id}", response_model=Post, status_code=status.HTTP_200_OK)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    use_case: UpdatePostUseCase = Depends()
) -> Post:
    """Обновить пост"""
    try:
        return await use_case.execute(post_id=post_id, post_data=post_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )
    except PostNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.get_detail()
        )
    except PostTitleEmptyException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.get_detail()
        )
    except PostTextEmptyException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.get_detail()
        )
    except PostAuthorNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # 404, а не 400
            detail=e.get_detail()
        )
    except PostCategoryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # 404, а не 400
            detail=e.get_detail()
        )
    except PostLocationNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # 404, а не 400
            detail=e.get_detail()
        )
    except DatabaseOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e._detail or "Внутренняя ошибка сервера"
        )


@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(
    post_id: int,
    use_case: DeletePostUseCase = Depends()
) -> dict:
    """Удалить пост по ID"""
    try:
        return await use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.get_detail()
        )
    except DatabaseOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e._detail or "Внутренняя ошибка сервера"
        )