import uuid
from datetime import datetime
from typing import Optional

import phonenumbers
from pydantic import BaseModel, EmailStr, ValidationInfo, field_validator


class AccountUserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password_hash: Optional[str] = None
    country_code: Optional[str] = "IN"
    phone: Optional[str] = None


class AccountUserCreate(AccountUserBase):
    name: str
    email: EmailStr
    username: Optional[str] = None
    password_hash: str
    country_code: str
    phone: str

    @field_validator("phone")
    def validate_phone(cls, phone: str, info: ValidationInfo) -> str:
        country_code = info.data.get("country_code")
        if not country_code:
            raise ValueError("Country code is required for phone validation")
        try:
            parsed_number = phonenumbers.parse(phone, country_code)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError("Invalid phone number")
        except phonenumbers.NumberParseException as e:
            raise ValueError(f"Phone number parse error: {e}")
        return phone

    @field_validator("username", mode="before")
    def default_username(cls, username: Optional[str], info: ValidationInfo) -> str:
        if username and str(username).strip():  # If username is provided
            return str(username)
        email = info.data.get("email")
        if not email:
            raise ValueError("Email is required to generate default username")
        # Set default username as email before '@'
        return str(email.split("@")[0])


class AccountUserUpdate(AccountUserBase):
    name: Optional[str] = None
    password_hash: Optional[str] = None


class AccountUserInDBBase(AccountUserBase):
    id: uuid.UUID
    created_on: datetime
    is_active: bool
    last_logged_in: datetime
    updated_on: datetime

    class Config:
        from_attributes = True


class AccountUser(AccountUserInDBBase):
    pass
