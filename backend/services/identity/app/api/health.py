import schemas
from core.config import settings
from fastapi import APIRouter, FastAPI

health_api = FastAPI(
    title="Health Check",
    description="Health and liveness probe for Service Endpoint...",
)
health_router = APIRouter()


@health_router.get(
    "/",
    summary="Health and liveness probe for Service",
    response_model=schemas.HealthResponse,
)
async def health_probe() -> schemas.HealthResponse:
    """
    API Endpoint to check the application microservice health

    Returns:
        schemas.HealthResponse: HTTP response object consisting of the service health status
    """
    # TODO: Scanning all dependencies associated with the microservice with threshold definitions for performance
    #  1. Database -> Check connection and health
    #  2. Cache -> Check connection
    #  3. Message Queue -> Check connection and health
    #  4. Workers -> Check health

    return schemas.HealthResponse(
        status=schemas.HealthStatus.OK.value,
        service=settings.SERVICE_NAME,
        dependencies=None,
    )


health_api.include_router(router=health_router)
