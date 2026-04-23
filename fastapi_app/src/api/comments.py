from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import ValidationError
from src.schemas.comments import Comment, CommentCreate, CommentUpdate
from src.domain.comments.use_cases.get_comment_by_id import GetCommentByIdUseCase
from src.domain.comments.use_cases.create_comment import CreateCommentUseCase
from src.domain.comments.use_cases.update_comment import UpdateCommentUseCase
from src.domain.comments.use_cases.delete_comment import DeleteCommentUseCase
from src.core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException,
    CommentAuthorNotFoundException,
    CommentPostNotFoundException,
    CommentTextEmptyException
)

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/{comment_id}", response_model=Comment, status_code=status.HTTP_200_OK)
async def get_comment_by_id(
    comment_id: int,
    use_case: GetCommentByIdUseCase = Depends()
) -> Comment:
    """Получить комментарий по ID"""
    try:
        return await use_case.execute(comment_id=comment_id)
    except CommentNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.get_detail()
        )


@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    use_case: CreateCommentUseCase = Depends()
) -> Comment:
    """Создать новый комментарий"""
    try:
        return await use_case.execute(comment_data=comment_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )
    except CommentAuthorNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.get_detail()
        )
    except CommentPostNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.get_detail()
        )
    except CommentTextEmptyException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.get_detail()
        )


@router.put("/{comment_id}", response_model=Comment, status_code=status.HTTP_200_OK)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    use_case: UpdateCommentUseCase = Depends()
) -> Comment:
    """Обновить комментарий"""
    try:
        return await use_case.execute(comment_id=comment_id, comment_data=comment_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )
    except CommentNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.get_detail()
        )
    except CommentTextEmptyException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.get_detail()
        )


@router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment(
    comment_id: int,
    use_case: DeleteCommentUseCase = Depends()
) -> dict:
    """Удалить комментарий"""
    try:
        return await use_case.execute(comment_id=comment_id)
    except CommentNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.get_detail()
        )