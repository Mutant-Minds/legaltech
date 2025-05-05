from typing import Any, List, Optional

from pydantic import PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    PROJECT_NAME: str
    SERVICE_NAME: str
    VERSION: str
    DEBUG: Optional[bool] = False
    ENVIRONMENT: str
    API_NAME: str
    API_VERSION: str
    ROOT_PATH: Optional[str] = None

    @staticmethod
    def assemble_path(v: Optional[str], values: ValidationInfo) -> Any:
        if not v:
            return f"/{values.data.get('API_NAME')}/{values.data.get('API_VERSION')}"
        return v

    _validate_paths = field_validator("ROOT_PATH", mode="before")(assemble_path)

    BACKEND_CORS_ORIGINS: List[str] = []

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=values.data.get("POSTGRES_USER"),
                password=values.data.get("POSTGRES_PASSWORD"),
                host=values.data.get("POSTGRES_SERVER"),
                path=f"{values.data.get('POSTGRES_DB') or ''}",
            )
        )
