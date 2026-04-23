from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.infrastructure.sqlite.repositories.users_repository import UsersRepository
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.schemas.comments import Comment as CommentSchema, CommentCreate
from src.core.exceptions.database_exceptions import (
    UserNotFoundException,
    PostNotFoundException,
    CommentAuthorNotFoundExceptionDB,
    CommentPostNotFoundExceptionDB
)
from src.core.exceptions.domain_exceptions import (
    CommentAuthorNotFoundException,
    CommentPostNotFoundException
)


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._user_repo = UsersRepository()
        self._post_repo = PostRepository()

    async def execute(self, comment_data: CommentCreate) -> CommentSchema:
        try:
            with self._database.session() as session:
                # Проверяем существование автора
                try:
                    author = self._user_repo.get_by_id(session, comment_data.author_id)
                except UserNotFoundException:
                    raise CommentAuthorNotFoundExceptionDB()

                # Проверяем существование поста
                try:
                    post = self._post_repo.get_by_id(session, comment_data.post_id)
                except PostNotFoundException:
                    raise CommentPostNotFoundExceptionDB()

                # Создаем комментарий
                comment = self._repo.create(session=session, comment_data=comment_data)
        except CommentAuthorNotFoundExceptionDB:
            raise CommentAuthorNotFoundException(author_id=comment_data.author_id)
        except CommentPostNotFoundExceptionDB:
            raise CommentPostNotFoundException(post_id=comment_data.post_id)

        return CommentSchema.model_validate(obj=comment)