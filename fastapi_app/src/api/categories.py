from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import ValidationError
from src.schemas.categories import Category, CategoryCreate, CategoryUpdate
from src.domain.categories.use_cases.get_category_by_id import GetCategoryByIdUseCase
from src.domain.categories.use_cases.create_category import CreateCategoryUseCase
from src.domain.categories.use_cases.update_category import UpdateCategoryUseCase
from src.domain.categories.use_cases.delete_category import DeleteCategoryUseCase
from src.core.exceptions.database_exceptions import DatabaseOperationError
from src.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    CategorySlugIsNotUniqueException,
    CategoryTitleIsNotUniqueException,
    CategoryTitleEmptyException,
    CategorySlugEmptyException
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/{category_id}", response_model=Category, status_code=status.HTTP_200_OK)
async def get_category_by_id(
    category_id: int,
    use_case: GetCategoryByIdUseCase = Depends()
) -> Category:
    """Получить категорию по ID"""
    try:
        return await use_case.execute(category_id=category_id)
    except CategoryNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.get_detail()
        )
    except DatabaseOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e._detail or "Внутренняя ошибка сервера"
        )


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    use_case: CreateCategoryUseCase = Depends()
) -> Category:
    """Создать новую категорию"""
    try:
        return await use_case.execute(category_data=category_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )
    except CategoryTitleEmptyException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.get_detail()
        )
    except CategorySlugEmptyException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.get_detail()
        )
    except CategorySlugIsNotUniqueException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.get_detail()
        )
    except DatabaseOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e._detail or "Внутренняя ошибка сервера"
        )
    except CategoryTitleIsNotUniqueException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.get_detail()
        )


@router.put("/{category_id}", response_model=Category, status_code=status.HTTP_200_OK)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    use_case: UpdateCategoryUseCase = Depends()
) -> Category:
    """Обновить категорию"""
    try:
        return await use_case.execute(category_id=category_id, category_data=category_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )
    except CategoryNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.get_detail()
        )
    except CategoryTitleEmptyException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.get_detail()
        )
    except CategorySlugEmptyException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.get_detail()
        )
    except CategorySlugIsNotUniqueException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.get_detail()
        )
    except DatabaseOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e._detail or "Внутренняя ошибка сервера"
        )
    except CategoryTitleIsNotUniqueException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.get_detail()
        )


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(
    category_id: int,
    use_case: DeleteCategoryUseCase = Depends()
) -> dict:
    """Удалить категорию по ID"""
    try:
        return await use_case.execute(category_id=category_id)
    except CategoryNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.get_detail()
        )
    except DatabaseOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e._detail or "Внутренняя ошибка сервера"
        )