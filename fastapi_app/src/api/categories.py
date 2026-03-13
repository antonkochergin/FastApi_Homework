from fastapi import APIRouter, status
from fastapi_app.src.schemas.categories import Category, CategoryCreate, CategoryUpdate
from fastapi_app.src.domain.categories_use_cases.create_category import CreateCategoryUseCase
from fastapi_app.src.domain.categories_use_cases.get_category import GetCategoryUseCase
from fastapi_app.src.domain.categories_use_cases.update_category import UpdateCategoryUseCase
from fastapi_app.src.domain.categories_use_cases.delete_category import DeleteCategoryUseCase

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(category_data: CategoryCreate) -> Category:
    """Создать новую категорию"""
    use_case = CreateCategoryUseCase()
    return await use_case.execute(category_data=category_data)


@router.get("/{category_id}", response_model=Category, status_code=status.HTTP_200_OK)
async def get_category(category_id: int) -> Category:
    """Получить категорию по ID"""
    use_case = GetCategoryUseCase()
    return await use_case.execute(category_id=category_id)


@router.put("/{category_id}", response_model=Category, status_code=status.HTTP_200_OK)
async def update_category(category_id: int, category_data: CategoryUpdate) -> Category:
    """Обновить категорию"""
    use_case = UpdateCategoryUseCase()
    return await use_case.execute(category_id=category_id, category_data=category_data)


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(category_id: int) -> dict:
    """Удалить категорию"""
    use_case = DeleteCategoryUseCase()
    return await use_case.execute(category_id=category_id)