from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from core.config import settings
from fastapi import Depends, Request
from specter import crud, models, utils
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# Create the async engine
engine: AsyncEngine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, echo=True
)

# Create a sessionmaker for AsyncSession
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_tenant(request: Request) -> models.Tenant:
    """
    Extracts the tenant based on the host header.

    Args:
        request:

    Returns:
        tenant

    Raises:
        TenantNotFoundError: if no tenant is found.
    """
    host_wo_port = request.headers["host"].split(":", 1)[0]
    async with with_db(None) as db:
        tenant = crud.tenant.get_by_host(db=db, host=host_wo_port)
    if not tenant:
        raise utils.TenantNotFoundError(host=host_wo_port)
    return tenant


@asynccontextmanager
async def with_db(tenant_schema: Optional[str]) -> AsyncGenerator[AsyncSession, None]:
    """
    Async context manager for AsyncSession, optionally using a schema_translate_map.

    Args:
        tenant_schema:

    Returns:

    """
    schema_translate_map = dict(tenant=tenant_schema) if tenant_schema else None
    connectable = engine.execution_options(schema_translate_map=schema_translate_map)
    async with AsyncSessionLocal(bind=connectable) as session:
        try:
            yield session
        finally:
            await session.close()


async def get_db(
    tenant: models.Tenant = Depends(get_tenant),
) -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to provide an AsyncSession scoped to the tenant's schema.

    Args:
        tenant:

    Returns:

    """
    async with with_db(tenant.schema) as db:
        yield db


async def get_shared_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to provide an AsyncSession for the shared/public schema.
    Use this for shared tables (e.g., account_user, tenant).

    Returns:

    """
    async with with_db(None) as db:
        yield db
