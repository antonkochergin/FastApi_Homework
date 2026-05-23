from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from core.exceptions.api_exceptions import NotFoundByFieldException
from core.exceptions.domain_exceptions import (
    InvalidPasswordException,
    UserNotFoundByUsernameException,
)
from core.logging import get_logger
from domain.auth.use_cases import AuthenticateUserUseCase, CreateAccessTokenUseCase
from schemas.auth import Token

router = APIRouter()
logger = get_logger(__name__)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_use_case: Annotated[AuthenticateUserUseCase, Depends()],
    create_token_use_case: CreateAccessTokenUseCase = Depends(),
) -> Token:
    try:
        user = await auth_use_case.execute(
            username=form_data.username, password=form_data.password
        )
    except InvalidPasswordException as exc:
        raise HTTPException(
            status_code=exc.get_status_code(),
            detail=exc.get_detail(),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except UserNotFoundByUsernameException as exc:
        logger.error(f"{exc.get_status_code()} - failed to create token: {exc.get_detail()}")
        raise NotFoundByFieldException(exc)

    access_token = await create_token_use_case.execute(username=user.username)

    return Token(access_token=access_token, token_type="bearer")
