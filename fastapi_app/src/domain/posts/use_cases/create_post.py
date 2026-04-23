from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.infrastructure.sqlite.repositories.users_repository import UsersRepository
from src.infrastructure.sqlite.repositories.category_repository import CategoryRepository
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.schemas.posts import Post as PostSchema, PostCreate
from src.core.exceptions.database_exceptions import (
    PostAuthorNotFoundExceptionDB,
    PostCategoryNotFoundExceptionDB,
    PostLocationNotFoundExceptionDB,
    DatabaseOperationError,
    UserNotFoundException,
    CategoryNotFoundException,
    LocationNotFoundException
)
from src.core.exceptions.domain_exceptions import (
    PostAuthorNotFoundException,
    PostCategoryNotFoundException,
    PostLocationNotFoundException,
    PostTitleEmptyException,
    PostTextEmptyException
)


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UsersRepository()
        self._category_repo = CategoryRepository()
        self._location_repo = LocationRepository()

    async def execute(self, post_data: PostCreate) -> PostSchema:
        # Проверка на пустой заголовок
        if not post_data.title or not post_data.title.strip():
            raise PostTitleEmptyException()

        # Проверка на пустое содержание
        if not post_data.text or not post_data.text.strip():
            raise PostTextEmptyException()

        try:
            with self._database.session() as session:
                # Проверяем существование автора
                try:
                    author = self._user_repo.get_by_id(session, post_data.author_id)
                except UserNotFoundException:
                    raise PostAuthorNotFoundException(author_id=post_data.author_id)

                # Проверяем существование категории (если указана)
                if post_data.category_id:
                    try:
                        category = self._category_repo.get_by_id(session, post_data.category_id)
                    except CategoryNotFoundException:
                        raise PostCategoryNotFoundException(category_id=post_data.category_id)

                # Проверяем существование локации (если указана)
                if post_data.location_id:
                    try:
                        location = self._location_repo.get_by_id(session, post_data.location_id)
                    except LocationNotFoundException:
                        raise PostLocationNotFoundException(location_id=post_data.location_id)

                # Создаем пост
                post = self._repo.create(session, post_data)
        except PostAuthorNotFoundExceptionDB:
            raise PostAuthorNotFoundException(author_id=post_data.author_id)
        except PostCategoryNotFoundExceptionDB:
            raise PostCategoryNotFoundException(category_id=post_data.category_id)
        except PostLocationNotFoundExceptionDB:
            raise PostLocationNotFoundException(location_id=post_data.location_id)
        except DatabaseOperationError:
            raise

        return PostSchema.model_validate(obj=post)