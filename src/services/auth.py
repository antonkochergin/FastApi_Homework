from typing import Annotated

from fastapi import Depends
from jose import JWTError, jwt

from core.config import settings
from core.exceptions.auth_exceptions import CredentialsException
from core.exceptions.database_exceptions import NotFoundException
from infrastructure.postgres.database import Database
from infrastructure.postgres.database import database as postgres_database
from infrastructure.postgres.repositories import UserRepository
from resources.auth import oauth2_scheme
from schemas.user import UserResponse

AUTH_EXCEPTION_MESSAGE = "Authorization data cannot be verified"


class AuthService:
    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        _database: Database = postgres_database

        try:
            payload = jwt.decode(
                token=token,
                key=settings.SECRET_AUTH_KEY,
                algorithms=[settings.AUTH_ALGORITHM],
            )
            username: str = payload.get("sub")
            if username is None:
                raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)
        except JWTError:
            raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)

        async with _database.session() as session:
            try:
                repo = UserRepository(session)
                user = await repo.get_by_username(username=username)
            except NotFoundException:
                raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)

            return UserResponse.model_validate(obj=user)
