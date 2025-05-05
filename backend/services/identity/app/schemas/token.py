from enum import Enum

from pydantic import BaseModel


class TokenType(str, Enum):
    BEARER = "bearer"


class Token(BaseModel):
    access_token: str
    token_type: TokenType


class TokenPayload(BaseModel):
    pass
