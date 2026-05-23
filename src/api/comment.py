from typing import List

from fastapi import APIRouter, Depends, status

from core.exceptions.api_exceptions import NotFoundByFieldException, PermissionDeniedException
from core.exceptions.domain_exceptions import (
    CommentNotFoundException,
    DomainPermissionDeniedException,
    PostNotFoundException,
)
from core.logging import get_logger
from domain.comment.use_cases import *
from schemas.comment import CommentCreate, CommentResponse, CommentUpdate
from schemas.user import UserResponse
from services.auth import AuthService

router = APIRouter()
logger = get_logger(__name__)


@router.get("/comments/", response_model=List[CommentResponse], status_code=status.HTTP_200_OK)
async def get_all_comments(use_case: GetCommentsUseCase = Depends()) -> List[CommentResponse]:
    return await use_case.execute()


@router.get(
    "/comments/{comment_id}", response_model=CommentResponse, status_code=status.HTTP_200_OK
)
async def get_comment(comment_id: int, use_case: GetCommentUseCase = Depends()) -> CommentResponse:
    try:
        return await use_case.execute(comment_id=comment_id)
    except CommentNotFoundException as exc:
        raise NotFoundByFieldException(exc)


@router.post("/comments/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    user: UserResponse = Depends(AuthService.get_current_user),
    use_case: CreateCommentUseCase = Depends(),
) -> CommentResponse:
    try:
        return await use_case.execute(comment_data=comment_data, author_id=user.id)
    except PostNotFoundException as exc:
        logger.error(
            f"{exc.get_status_code()} - {user.username} failed to create comment: {exc.get_detail()}"
        )
        raise NotFoundByFieldException(exc)


@router.put(
    "/comments/{comment_id}", response_model=CommentResponse, status_code=status.HTTP_200_OK
)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    user: UserResponse = Depends(AuthService.get_current_user),
    use_case: UpdateCommentUseCase = Depends(),
) -> CommentResponse:
    try:
        return await use_case.execute(
            comment_id=comment_id, comment_data=comment_data, current_user=user
        )
    except DomainPermissionDeniedException as exc:
        logger.error(f"{exc.get_status_code()} - {user.username}: {exc.get_detail()}")
        raise PermissionDeniedException(exc)
    except CommentNotFoundException as exc:
        logger.error(
            f"{exc.get_status_code()} - {user.username} failed to update comment: {exc.get_detail()}"
        )
        raise NotFoundByFieldException(exc)


@router.delete(
    "/comments/{comment_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_comment(
    comment_id: int,
    user: UserResponse = Depends(AuthService.get_current_user),
    use_case: DeleteCommentUseCase = Depends(),
) -> None:
    try:
        return await use_case.execute(comment_id=comment_id, current_user=user)
    except DomainPermissionDeniedException as exc:
        logger.error(f"{exc.get_status_code()} - {user.username}: {exc.get_detail()}")
        raise PermissionDeniedException(exc)
    except CommentNotFoundException as exc:
        logger.error(
            f"{exc.get_status_code()} - {user.username} failed to delete comment: {exc.get_detail()}"
        )
        raise NotFoundByFieldException(exc)
