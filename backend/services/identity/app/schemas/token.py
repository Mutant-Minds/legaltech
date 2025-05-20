from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel


class TokenType(str, Enum):
    BEARER = "bearer"


class Token(BaseModel):
    access_token: str
    token_type: TokenType


class TokenPayload(BaseModel):
    sub: str
    exp: datetime
    aud: str
    claims: Optional[Dict[str, Any]]
