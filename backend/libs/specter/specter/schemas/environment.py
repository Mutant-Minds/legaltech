from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT: str = "development"
    STAGING: str = "staging"
    PRODUCTION: str = "production"
    QA: str = "qa"
    TEST: str = "test"
    LOCAL: str = "local"
