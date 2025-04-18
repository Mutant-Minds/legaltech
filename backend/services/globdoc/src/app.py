from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from specter.apiutil.exception_handler import register_handlers

from api.health import health_api
from core.config import settings


@asynccontextmanager
async def lifespan(fastapi: FastAPI) -> AsyncGenerator[None, None]:
    """
    Startup and Shutdown Events.

    Args:
        fastapi (FastAPI): The FastAPI instance (although not used directly here).

    Returns:
        None
    """
    try:
        yield
    except Exception as e:
        print(f"Unexpected exception encountered: {str(e)}")
        pass
    finally:
        pass


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="The **Global Document Repository (GDR)** is a centralized platform for storing, managing, and "
    "discovering legal documents across firms, teams, and jurisdictions.",
    openapi_url=f"{settings.ROOT_PATH}/openapi.json",
    version=settings.VERSION,
    docs_url=f"{settings.ROOT_PATH}/docs",
    redoc_url=f"{settings.ROOT_PATH}/redoc",
    lifespan=lifespan,
)

# Register Custom Exception/Error Handlers
register_handlers(app)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# MOUNTING ENDPOINTS
if settings.API_VERSION == "v1":
    from api.v1.api import apiv1_router

    app.include_router(apiv1_router, prefix=settings.ROOT_PATH)
else:
    raise RuntimeError("Invalid API Version")

app.mount(path="/health", app=health_api)
