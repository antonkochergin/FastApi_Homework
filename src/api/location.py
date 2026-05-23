from typing import List

from fastapi import APIRouter, Depends, status

from core.exceptions.api_exceptions import (
    AlreadyExistWithFieldException,
    NotFoundByFieldException,
    PermissionDeniedException,
)
from core.exceptions.domain_exceptions import (
    LocationNotFoundByNameException,
    LocationNotFoundException,
    LocationWithNameAlreadyExistException,
    NotEnoughRightsException,
)
from core.logging import get_logger
from domain.location.use_cases import *
from schemas.location import LocationCreate, LocationResponse
from schemas.user import UserResponse
from services.auth import AuthService

router = APIRouter()
logger = get_logger(__name__)


@router.get("/locations/", response_model=List[LocationResponse], status_code=status.HTTP_200_OK)
async def get_all_locations(use_case: GetLocationsUseCase = Depends()) -> List[LocationResponse]:
    return await use_case.execute()


@router.get(
    "/locations/{location_id}", response_model=LocationResponse, status_code=status.HTTP_200_OK
)
async def get_location(
    location_id: int, use_case: GetLocationUseCase = Depends()
) -> LocationResponse:
    try:
        return await use_case.execute(location_id=location_id)
    except LocationNotFoundException as exc:
        raise NotFoundByFieldException(exc)


@router.get(
    "/locations/by-name/{name}", response_model=LocationResponse, status_code=status.HTTP_200_OK
)
async def get_location_by_name(
    name: str, use_case: GetLocationBySlugUseCase = Depends()
) -> LocationResponse:
    try:
        return await use_case.execute(name=name)
    except LocationNotFoundByNameException as exc:
        raise NotFoundByFieldException(exc)


@router.post("/locations/", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
async def create_location(
    location_data: LocationCreate,
    user: UserResponse = Depends(AuthService.get_current_user),
    use_case: CreateLocationUseCase = Depends(),
) -> LocationResponse:
    try:
        return await use_case.execute(location_data=location_data, current_user=user)
    except NotEnoughRightsException as exc:
        logger.error(f"{exc.get_status_code()} - {exc.get_detail()}")
        raise PermissionDeniedException(exc)
    except LocationWithNameAlreadyExistException as exc:
        logger.error(
            f"{exc.get_status_code()} - {user.username} failed to create location: {exc.get_detail()}"
        )
        raise AlreadyExistWithFieldException(exc)


@router.delete(
    "/locations/{location_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_location(
    location_id: int,
    user: UserResponse = Depends(AuthService.get_current_user),
    use_case: DeleteLocationUseCase = Depends(),
) -> None:
    try:
        return await use_case.execute(location_id=location_id, current_user=user)
    except NotEnoughRightsException as exc:
        logger.error(f"{exc.get_status_code()} - {exc.get_detail()}")
        raise PermissionDeniedException(exc)
    except LocationNotFoundException as exc:
        logger.error(
            f"{exc.get_status_code()} - {user.username} failed to delete location: {exc.get_detail()}"
        )
        raise NotFoundByFieldException(exc)
