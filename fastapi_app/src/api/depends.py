from src.domain.users.use_cases.get_user_by_login import GetUserByLoginUseCase
from src.domain.users.use_cases.create_user import CreateUserUseCase
from src.domain.auth.use_cases.authenticate_user import AuthenticateUserUseCase
from src.domain.auth.use_cases.create_access_token import CreateAccessTokenUseCase


# ============ Users use cases ============
def get_get_user_by_login_use_case() -> GetUserByLoginUseCase:
    return GetUserByLoginUseCase()


def create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase()


# ============ Auth use cases ============
def authenticate_user_use_case() -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase()


def create_access_token_use_case() -> CreateAccessTokenUseCase:
    return CreateAccessTokenUseCase()