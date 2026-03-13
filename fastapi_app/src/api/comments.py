from fastapi import APIRouter, status
from fastapi_app.src.schemas.comments import Comment, CommentCreate, CommentUpdate
from fastapi_app.src.domain.comments_use_cases.create_comment import CreateCommentUseCase
from fastapi_app.src.domain.comments_use_cases.get_comment import GetCommentUseCase
from fastapi_app.src.domain.comments_use_cases.update_comment import UpdateCommentUseCase
from fastapi_app.src.domain.comments_use_cases.delete_comment import DeleteCommentUseCase

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(comment_data: CommentCreate) -> Comment:
    """Создать новый комментарий"""
    use_case = CreateCommentUseCase()
    return await use_case.execute(comment_data=comment_data)


@router.get("/{comment_id}", response_model=Comment, status_code=status.HTTP_200_OK)
async def get_comment(comment_id: int) -> Comment:
    """Получить комментарий по ID"""
    use_case = GetCommentUseCase()
    return await use_case.execute(comment_id=comment_id)


@router.put("/{comment_id}", response_model=Comment, status_code=status.HTTP_200_OK)
async def update_comment(comment_id: int, comment_data: CommentUpdate) -> Comment:
    """Обновить комментарий"""
    use_case = UpdateCommentUseCase()
    return await use_case.execute(comment_id=comment_id, comment_data=comment_data)


@router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment(comment_id: int) -> dict:
    """Удалить комментарий"""
    use_case = DeleteCommentUseCase()
    return await use_case.execute(comment_id=comment_id)