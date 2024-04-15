import functools
from typing import Optional

from pydantic import Field, ValidationInfo, field_validator
from pydantic_settings import BaseSettings
from sqlalchemy import URL


class Settings(BaseSettings):
    PG_HOST: str
    PG_USER: str
    PG_PASSWORD: str
    PG_DB: str
    PG_PORT: int
    PG_URI: Optional[URL] = Field(None)
    SECRET_KEY: str
    SALT: str
    ALGORITHM: str

    @field_validator("PG_URI", mode="after")
    def create_db_url(cls, value: Optional[URL], values: ValidationInfo):
        value: URL = URL.create(
            "postgresql+asyncpg",
            values.data.get("PG_USER"),
            values.data.get("PG_PASSWORD"),
            values.data.get("PG_HOST"),
            values.data.get("PG_PORT"),
            values.data.get("PG_DB"),
        )
        return value


@functools.lru_cache
def get_settings():
    return Settings()


Configs: Settings = get_settings()
