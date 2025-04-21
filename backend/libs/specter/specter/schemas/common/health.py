from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class HealthStatus(str, Enum):
    OK = "OK"
    DEGRADED = "DEGRADED"
    ERROR = "ERROR"


class Dependency(BaseModel):
    name: str
    status: HealthStatus
    details: Optional[str] = None


class HealthResponse(BaseModel):
    status: HealthStatus
    service: str
    dependencies: Optional[List[Dependency]] = None
