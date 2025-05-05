import uuid
from datetime import datetime

from pydantic import BaseModel


class TenantBase(BaseModel):
    pass


class TenantCreate(TenantBase):
    pass


class TenantUpdate(TenantBase):
    pass


class TenantInDBBase(TenantBase):
    id: uuid.UUID
    created_on: datetime
    is_active: bool
    updated_on: datetime

    class Config:
        from_attributes = True


class Tenant(TenantInDBBase):
    pass
