from functools import lru_cache

from pydantic_settings import BaseSettings
from specter.core.config import CommonSettings


@lru_cache()
def retrieve_settings() -> BaseSettings:
    """
    Loads pydantic base settings via an env file and returns the settings object

    Returns:
        BaseSettings: Pydantic BaseSettings object
    """
    return Settings()


class Settings(CommonSettings):  # type: ignore[misc]
    pass


settings = retrieve_settings()
