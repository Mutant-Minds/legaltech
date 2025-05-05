import os
from functools import lru_cache

import schemas
from pydantic_settings import BaseSettings, SettingsConfigDict
from specter.core.config import CommonSettings


@lru_cache()
def retrieve_settings() -> BaseSettings:
    """
    Loads pydantic base settings via an env file and returns the settings object

    Returns:
        BaseSettings: Pydantic BaseSettings object
    """
    if os.getenv("ENVIRONMENT") == schemas.Environment.TEST.value:
        return TestSettings()
    return Settings()


class Settings(CommonSettings):  # type: ignore[misc]
    pass


class TestSettings(CommonSettings):  # type: ignore[misc]
    model_config = SettingsConfigDict(
        env_file=".env.test",
        env_file_encoding="utf-8",
    )


settings = retrieve_settings()
