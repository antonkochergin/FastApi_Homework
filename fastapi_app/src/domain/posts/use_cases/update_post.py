from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.infrastructure.sqlite.repositories.users_repository import UsersRepository
from src.infrastructure.sqlite.repositories.category_repository import CategoryRepository
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.schemas.posts import Post as PostSchema, PostUpdate
from src.core.exceptions.database_exceptions import (
    PostNotFoundException,
    PostAuthorNotFoundExceptionDB,
    PostCategoryNotFoundExceptionDB,
    PostLocationNotFoundExceptionDB,
    DatabaseOperationError,
    UserNotFoundException,
    CategoryNotFoundException,
    LocationNotFoundException
)
from src.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    PostAuthorNotFoundException,
    PostCategoryNotFoundException,
    PostLocationNotFoundException,
    PostTitleEmptyException,
    PostTextEmptyException
)


class UpdatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UsersRepository()
        self._category_repo = CategoryRepository()
        self._location_repo = LocationRepository()

    async def execute(self, post_id: int, post_data: PostUpdate) -> PostSchema:
        try:
            with self._database.session() as session:
                # Получаем существующий пост
                try:
                    existing_post = self._repo.get_by_id(session, post_id)
                except PostNotFoundException:
                    raise PostNotFoundByIdException(post_id=post_id)

                # Проверяем заголовок на пустоту
                if post_data.title is not None:
                    if not post_data.title or not post_data.title.strip():
                        raise PostTitleEmptyException()

                # Проверяем содержание на пустоту
                if post_data.text is not None:
                    if not post_data.text or not post_data.text.strip():
                        raise PostTextEmptyException()

                # Проверяем существование автора (если меняется)
                if post_data.author_id and post_data.author_id != existing_post.author_id:
                    try:
                        author = self._user_repo.get_by_id(session, post_data.author_id)
                    except UserNotFoundException:
                        raise PostAuthorNotFoundException(author_id=post_data.author_id)

                # Проверяем существование категории (если меняется и указана)
                if post_data.category_id is not None and post_data.category_id != existing_post.category_id:
                    if post_data.category_id:  # если не None (может быть None для снятия категории)
                        try:
                            category = self._category_repo.get_by_id(session, post_data.category_id)
                        except CategoryNotFoundException:
                            raise PostCategoryNotFoundException(category_id=post_data.category_id)

                # Проверяем существование локации (если меняется и указана)
                if post_data.location_id is not None and post_data.location_id != existing_post.location_id:
                    if post_data.location_id:  # если не None (может быть None для снятия локации)
                        try:
                            location = self._location_repo.get_by_id(session, post_data.location_id)
                        except LocationNotFoundException:
                            raise PostLocationNotFoundException(location_id=post_data.location_id)

                # Обновляем пост
                post = self._repo.update(session, post_id, post_data)
        except PostAuthorNotFoundExceptionDB:
            raise PostAuthorNotFoundException(author_id=post_data.author_id)
        except PostCategoryNotFoundExceptionDB:
            raise PostCategoryNotFoundException(category_id=post_data.category_id)
        except PostLocationNotFoundExceptionDB:
            raise PostLocationNotFoundException(location_id=post_data.location_id)
        except DatabaseOperationError:
            raise

        return PostSchema.model_validate(obj=post)