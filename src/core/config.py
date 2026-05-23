from pathlib import Path
from typing import List

from pydantic import SecretStr
from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    ORIGINS: str
    PORT: int
    ROOT_PATH: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    AUTH_ALGORITHM: str
    SECRET_AUTH_KEY: str

    POSTGRES_SCHEMA: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRES_USER: SecretStr
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_RECONNECT_INTERVAL_SEC: int

    @property
    def postgres_url(self) -> str:
        creds = (
            f"{self.POSTGRES_USER.get_secret_value()}:{self.POSTGRES_PASSWORD.get_secret_value()}"
        )
        return f"postgresql+asyncpg://{creds}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def origins_list(self) -> List[str]:
        if not self.ORIGINS:
            return ["*"]
        return [origin.strip() for origin in self.ORIGINS.split(",")]

    class Config:
        env_file = PROJECT_ROOT / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
