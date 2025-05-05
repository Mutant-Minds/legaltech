from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, constr


class RegisterUser(BaseModel):
    name: str
    email: EmailStr
    username: Optional[str] = None
    password: Annotated[str, constr(min_length=8)]
    country_code: Optional[str] = None
    phone: Optional[str] = None
