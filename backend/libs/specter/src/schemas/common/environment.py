from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    QA = "qa"
    TEST = "test"
    LOCAL = "local"
