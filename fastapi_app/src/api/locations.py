from fastapi import APIRouter, Depends, Query, status, HTTPException
from pydantic import ValidationError
from src.schemas.locations import Location, LocationCreate, LocationUpdate
from src.domain.locations.use_cases.get_locations import GetLocationsUseCase
from src.domain.locations.use_cases.get_location_by_id import GetLocationByIdUseCase
from src.domain.locations.use_cases.create_location import CreateLocationUseCase
from src.domain.locations.use_cases.update_location import UpdateLocationUseCase
from src.domain.locations.use_cases.delete_location import DeleteLocationUseCase
from src.core.exceptions.database_exceptions import DatabaseOperationError
from src.core.exceptions.domain_exceptions import (
    LocationNotFoundByIdException,
    LocationNameIsNotUniqueException,
    LocationNameEmptyException
)

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/", response_model=list[Location], status_code=status.HTTP_200_OK)
async def get_locations(
    published_only: bool = Query(False, description="Только опубликованные"),
    use_case: GetLocationsUseCase = Depends()
) -> list[Location]:
    """Получить все локации"""
    try:
        return await use_case.execute(published_only=published_only)
    except DatabaseOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e._detail or "Внутренняя ошибка сервера"
        )


@router.get("/{location_id}", response_model=Location, status_code=status.HTTP_200_OK)
async def get_location_by_id(
    location_id: int,
    use_case: GetLocationByIdUseCase = Depends()
) -> Location:
    """Получить локацию по ID"""
    try:
        return await use_case.execute(location_id=location_id)
    except LocationNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.get_detail()
        )
    except DatabaseOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e._detail or "Внутренняя ошибка сервера"
        )


@router.post("/", response_model=Location, status_code=status.HTTP_201_CREATED)
async def create_location(
    location_data: LocationCreate,
    use_case: CreateLocationUseCase = Depends()
) -> Location:
    """Создать новую локацию"""
    try:
        return await use_case.execute(location_data=location_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )
    except LocationNameEmptyException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.get_detail()
        )
    except LocationNameIsNotUniqueException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.get_detail()
        )
    except DatabaseOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e._detail or "Внутренняя ошибка сервера"
        )


@router.put("/{location_id}", response_model=Location, status_code=status.HTTP_200_OK)
async def update_location(
    location_id: int,
    location_data: LocationUpdate,
    use_case: UpdateLocationUseCase = Depends()
) -> Location:
    """Обновить локацию"""
    try:
        return await use_case.execute(location_id=location_id, location_data=location_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )
    except LocationNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.get_detail()
        )
    except LocationNameEmptyException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.get_detail()
        )
    except LocationNameIsNotUniqueException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.get_detail()
        )
    except DatabaseOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e._detail or "Внутренняя ошибка сервера"
        )


@router.delete("/{location_id}", status_code=status.HTTP_200_OK)
async def delete_location(
    location_id: int,
    use_case: DeleteLocationUseCase = Depends()
) -> dict:
    """Удалить локацию"""
    try:
        return await use_case.execute(location_id=location_id)
    except LocationNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.get_detail()
        )
    except DatabaseOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e._detail or "Внутренняя ошибка сервера"
        )