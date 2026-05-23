from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import FileResponse

from core.exceptions.api_exceptions import (
    ImageException,
    NotFoundByFieldException,
    PermissionDeniedException,
)
from core.exceptions.domain_exceptions import (
    CategoryNotFoundException,
    DomainPermissionDeniedException,
    LocationNotFoundException,
    NotEnoughRightsException,
    PostHasNoImageException,
    PostNotFoundException,
    UploadFileIsNotImageException,
)
from core.logging import get_logger
from domain.post.use_cases import *
from schemas.post import PostCreate, PostImageResponse, PostResponse, PostUpdate
from schemas.user import UserResponse
from services.auth import AuthService

router = APIRouter()
logger = get_logger(__name__)


@router.get("/posts/", response_model=List[PostResponse], status_code=status.HTTP_200_OK)
async def get_all_posts(use_case: GetPostsUseCase = Depends()) -> List[PostResponse]:
    return await use_case.execute()


@router.get("/posts/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def get_post(post_id: int, use_case: GetPostUseCase = Depends()) -> PostResponse:
    try:
        return await use_case.execute(post_id=post_id)
    except PostNotFoundException as exc:
        raise NotFoundByFieldException(exc)


@router.get("/posts/{post_id}/image", status_code=status.HTTP_200_OK, response_class=FileResponse)
async def get_post_image(post_id: int, use_case: GetImageUseCase = Depends()):
    try:
        return await use_case.execute(post_id=post_id)
    except PostNotFoundException as exc:
        raise NotFoundByFieldException(exc)
    except PostHasNoImageException as exc:
        raise ImageException(exc)


@router.post(
    "/posts/{post_id}/image", status_code=status.HTTP_201_CREATED, response_model=PostImageResponse
)
async def add_post_image(
    post_id: int,
    image: UploadFile = File(...),
    user: dict = Depends(AuthService.get_current_user),
    use_case: AddImageUseCase = Depends(),
):
    try:
        return await use_case.execute(post_id=post_id, image=image, current_user=user)
    except PostNotFoundException as exc:
        raise NotFoundByFieldException(exc)
    except (PostHasNoImageException, UploadFileIsNotImageException) as exc:
        raise ImageException(exc)
    except NotEnoughRightsException as exc:
        raise PermissionDeniedException(exc)


@router.post("/posts/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    user: UserResponse = Depends(AuthService.get_current_user),
    use_case: CreatePostUseCase = Depends(),
) -> PostResponse:
    try:
        return await use_case.execute(post_data=post_data, author_id=user.id)
    except (CategoryNotFoundException, LocationNotFoundException) as exc:
        logger.error(
            f"{exc.get_status_code()} - {user.username} failed to create post: {exc.get_detail()}"
        )
        raise NotFoundByFieldException(exc)


@router.put("/posts/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    user: UserResponse = Depends(AuthService.get_current_user),
    use_case: UpdatePostUseCase = Depends(),
) -> PostResponse:
    try:
        return await use_case.execute(post_id=post_id, post_data=post_data, current_user=user)
    except DomainPermissionDeniedException as exc:
        logger.error(f"{exc.get_status_code()} - {user.username}: {exc.get_detail()}")
        raise PermissionDeniedException(exc)
    except (CategoryNotFoundException, LocationNotFoundException) as exc:
        logger.error(
            f"{exc.get_status_code()} - {user.username} failed to update post: {exc.get_detail()}"
        )
        raise NotFoundByFieldException(exc)


@router.delete("/posts/{post_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    user: UserResponse = Depends(AuthService.get_current_user),
    use_case: DeletePostUseCase = Depends(),
) -> None:
    try:
        return await use_case.execute(post_id=post_id, current_user=user)
    except DomainPermissionDeniedException as exc:
        logger.error(f"{exc.get_status_code()} - {user.username}: {exc.get_detail()}")
        raise PermissionDeniedException(exc)
    except PostNotFoundException as exc:
        logger.error(
            f"{exc.get_status_code()} - {user.username} failed to delete post: {exc.get_detail()}"
        )
        raise NotFoundByFieldException(exc)
