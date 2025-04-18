from pydantic import BaseModel


class ErrorMessage(BaseModel):
    detail: str


class UnauthorizedMessage(BaseModel):
    detail: str
