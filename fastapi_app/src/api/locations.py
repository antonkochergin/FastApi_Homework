from fastapi import APIRouter, status
from fastapi_app.src.schemas.locations import Location, LocationCreate, LocationUpdate
from fastapi_app.src.domain.locations_use_cases.create_location import CreateLocationUseCase
from fastapi_app.src.domain.locations_use_cases.get_location import GetLocationUseCase
from fastapi_app.src.domain.locations_use_cases.update_location import UpdateLocationUseCase
from fastapi_app.src.domain.locations_use_cases.delete_location import DeleteLocationUseCase

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.post("/", response_model=Location, status_code=status.HTTP_201_CREATED)
async def create_location(location_data: LocationCreate) -> Location:
    """Создать новую локацию"""
    use_case = CreateLocationUseCase()
    return await use_case.execute(location_data=location_data)


@router.get("/{location_id}", response_model=Location, status_code=status.HTTP_200_OK)
async def get_location(location_id: int) -> Location:
    """Получить локацию по ID"""
    use_case = GetLocationUseCase()
    return await use_case.execute(location_id=location_id)


@router.put("/{location_id}", response_model=Location, status_code=status.HTTP_200_OK)
async def update_location(location_id: int, location_data: LocationUpdate) -> Location:
    """Обновить локацию"""
    use_case = UpdateLocationUseCase()
    return await use_case.execute(location_id=location_id, location_data=location_data)


@router.delete("/{location_id}", status_code=status.HTTP_200_OK)
async def delete_location(location_id: int) -> dict:
    """Удалить локацию"""
    use_case = DeleteLocationUseCase()
    return await use_case.execute(location_id=location_id)