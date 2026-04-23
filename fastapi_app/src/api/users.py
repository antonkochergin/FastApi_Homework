from fastapi import APIRouter, status, HTTPException, Depends

from src.schemas.users import User, UserCreate, UserUpdate
from src.domain.users.use_cases.get_user_by_login import GetUserByLoginUseCase
from src.domain.users.use_cases.create_user import CreateUserUseCase
from src.domain.users.use_cases.get_user_by_id import GetUserByIdUseCase
from src.domain.users.use_cases.get_user_by_username import GetUserByUsernameUseCase
from src.domain.users.use_cases.get_users import GetUsersUseCase
from src.domain.users.use_cases.update_user import UpdateUserUseCase
from src.domain.users.use_cases.delete_user import DeleteUserUseCase
from src.api.depends import (
    get_get_user_by_login_use_case,
    create_user_use_case,
)
from src.core.exceptions.domain_exceptions import (
    UserNotFoundByLoginException,
    UserNotFoundByIdException,
    UserNotFoundByUsernameException,
    UserUsernameIsNotUniqueException,
    UserEmailIsNotUniqueException,
)
from src.services.auth import AuthService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/by-login/{login}",
    status_code=status.HTTP_200_OK,
    response_model=User,
)
async def get_user_by_login(
    login: str,
    user: User = Depends(AuthService.get_current_user),
    use_case: GetUserByLoginUseCase = Depends(get_get_user_by_login_use_case),
) -> User:
    try:
        return await use_case.execute(login=login)
    except UserNotFoundByLoginException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())


@router.get(
    "/by-username/{username}",
    status_code=status.HTTP_200_OK,
    response_model=User,
)
async def get_user_by_username(
    username: str,
    user: User = Depends(AuthService.get_current_user),
    use_case: GetUserByUsernameUseCase = Depends(),
) -> User:
    try:
        return await use_case.execute(username=username)
    except UserNotFoundByUsernameException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=User,
)
async def get_user_by_id(
    user_id: int,
    user: User = Depends(AuthService.get_current_user),
    use_case: GetUserByIdUseCase = Depends(),
) -> User:
    try:
        return await use_case.execute(user_id=user_id)
    except UserNotFoundByIdException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[User],
)
async def get_users(
    user: User = Depends(AuthService.get_current_user),
    use_case: GetUsersUseCase = Depends(),
) -> list[User]:
    return await use_case.execute()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
)
async def create_user(
    user_data: UserCreate,
    use_case: CreateUserUseCase = Depends(create_user_use_case),
) -> User:
    try:
        return await use_case.execute(user_data=user_data)
    except UserUsernameIsNotUniqueException as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail())
    except UserEmailIsNotUniqueException as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail())


@router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=User,
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user: User = Depends(AuthService.get_current_user),
    use_case: UpdateUserUseCase = Depends(),
) -> User:
    try:
        return await use_case.execute(user_id=user_id, user_data=user_data)
    except UserNotFoundByIdException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())
    except (UserUsernameIsNotUniqueException, UserEmailIsNotUniqueException) as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail())


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    user_id: int,
    user: User = Depends(AuthService.get_current_user),
    use_case: DeleteUserUseCase = Depends(),
) -> dict:
    try:
        return await use_case.execute(user_id=user_id)
    except UserNotFoundByIdException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())