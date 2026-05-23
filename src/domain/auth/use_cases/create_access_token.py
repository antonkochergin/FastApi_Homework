from datetime import datetime, timedelta, timezone

from jose import jwt

from core.config import settings


class CreateAccessTokenUseCase:
    def __init__(self, token_expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES) -> None:
        self._ACCESS_TOKEN_EXPIRE_MINUTES = token_expire_minutes

    async def execute(self, username: str, expires_delta: timedelta | None = None) -> str:
        to_encode = {"sub": username}
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self._ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(
            claims=to_encode,
            key=settings.SECRET_AUTH_KEY,
            algorithm=settings.AUTH_ALGORITHM,
        )

        return encode_jwt
