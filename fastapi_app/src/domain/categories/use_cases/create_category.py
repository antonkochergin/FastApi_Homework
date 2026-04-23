from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category_repository import CategoryRepository
from src.schemas.categories import Category as CategorySchema, CategoryCreate
from src.core.exceptions.database_exceptions import (
    CategoryAlreadyExistsException,
    DatabaseOperationError
)
from src.core.exceptions.domain_exceptions import (
    CategorySlugIsNotUniqueException,
    CategoryTitleIsNotUniqueException,
    CategoryTitleEmptyException,
    CategorySlugEmptyException
)


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_data: CategoryCreate) -> CategorySchema:
        # Проверка на пустой title
        if not category_data.title or not category_data.title.strip():
            raise CategoryTitleEmptyException()

        # Проверка на пустой slug
        if not category_data.slug or not category_data.slug.strip():
            raise CategorySlugEmptyException()

        try:
            with self._database.session() as session:
                # Проверяем уникальность title
                existing_title = self._repo.get_by_title(session, category_data.title)
                if existing_title:
                    raise CategoryTitleIsNotUniqueException(title=category_data.title)

                # Проверяем уникальность slug
                existing_slug = self._repo.get_by_slug(session, category_data.slug)
                if existing_slug:
                    raise CategorySlugIsNotUniqueException(slug=category_data.slug)

                category = self._repo.create(session, category_data)
        except CategoryAlreadyExistsException:
            # Если IntegrityError, определяем что именно нарушено
            raise CategorySlugIsNotUniqueException(slug=category_data.slug)
        except DatabaseOperationError:
            raise

        return CategorySchema.model_validate(obj=category)