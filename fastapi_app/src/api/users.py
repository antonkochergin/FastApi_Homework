from fastapi import APIRouter, status
from fastapi_app.src.schemas.users import User, UserCreate, UserUpdate
from fastapi_app.src.domain.users_use_cases.create_user import CreateUserUseCase
from fastapi_app.src.domain.users_use_cases.get_user import GetUserUseCase
from fastapi_app.src.domain.users_use_cases.get_user_by_username import GetUserByUsernameUseCase
from fastapi_app.src.domain.users_use_cases.get_all_users import GetAllUsersUseCase
from fastapi_app.src.domain.users_use_cases.update_user import UpdateUserUseCase
from fastapi_app.src.domain.users_use_cases.delete_user import DeleteUserUseCase

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate) -> User:
    """Создать нового пользователя"""
    use_case = CreateUserUseCase()
    return await use_case.execute(user_data=user_data)


@router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user(user_id: int) -> User:
    """Получить пользователя по ID"""
    use_case = GetUserUseCase()
    return await use_case.execute(user_id=user_id)


@router.get("/username/{username}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user_by_username(username: str) -> User:
    """Получить пользователя по username"""
    use_case = GetUserByUsernameUseCase()
    return await use_case.execute(username=username)


@router.get("/", response_model=list[User], status_code=status.HTTP_200_OK)
async def get_all_users(skip: int = 0, limit: int = 100) -> list[User]:
    """Получить всех пользователей"""
    use_case = GetAllUsersUseCase()
    return await use_case.execute(skip=skip, limit=limit)


@router.put("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user_data: UserUpdate) -> User:
    """Обновить пользователя"""
    use_case = UpdateUserUseCase()
    return await use_case.execute(user_id=user_id, user_data=user_data)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int) -> dict:
    """Удалить пользователя"""
    use_case = DeleteUserUseCase()
    return await use_case.execute(user_id=user_id)