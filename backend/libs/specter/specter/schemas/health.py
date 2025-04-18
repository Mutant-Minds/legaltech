from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class HealthStatus(str, Enum):
    OK: str = "OK"
    DEGRADED: str = "DEGRADED"
    ERROR: str = "ERROR"


class Dependency(BaseModel):
    name: str
    status: HealthStatus
    details: Optional[str] = None


class HealthResponse(BaseModel):
    status: HealthStatus
    service: str
    dependencies: Optional[List[Dependency]] = None
