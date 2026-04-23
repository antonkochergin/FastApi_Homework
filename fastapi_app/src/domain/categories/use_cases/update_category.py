from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category_repository import CategoryRepository
from src.schemas.categories import Category as CategorySchema, CategoryUpdate
from src.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    CategoryAlreadyExistsException,
    DatabaseOperationError
)
from src.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    CategorySlugIsNotUniqueException,
    CategoryTitleIsNotUniqueException,
    CategoryTitleEmptyException,
    CategorySlugEmptyException
)


class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int, category_data: CategoryUpdate) -> CategorySchema:
        try:
            with self._database.session() as session:
                # Получаем существующую категорию
                try:
                    existing_category = self._repo.get_by_id(session, category_id)
                except CategoryNotFoundException:
                    raise CategoryNotFoundByIdException(category_id=category_id)

                # Проверяем title на пустоту
                if category_data.title is not None:
                    if not category_data.title or not category_data.title.strip():
                        raise CategoryTitleEmptyException()

                # Проверяем slug на пустоту
                if category_data.slug is not None:
                    if not category_data.slug or not category_data.slug.strip():
                        raise CategorySlugEmptyException()

                # Проверяем уникальность title
                if category_data.title and category_data.title != existing_category.title:
                    same_title = self._repo.get_by_title(session, category_data.title)
                    if same_title:
                        raise CategoryTitleIsNotUniqueException(title=category_data.title)

                # Проверяем уникальность slug
                if category_data.slug and category_data.slug != existing_category.slug:
                    same_slug = self._repo.get_by_slug(session, category_data.slug)
                    if same_slug:
                        raise CategorySlugIsNotUniqueException(slug=category_data.slug)

                # Обновляем категорию
                category = self._repo.update(session, category_id, category_data)
        except CategoryAlreadyExistsException:
            raise CategorySlugIsNotUniqueException(slug=category_data.slug)

        return CategorySchema.model_validate(obj=category)