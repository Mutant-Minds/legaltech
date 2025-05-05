from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from specter.utils import TenantNotFoundError
from starlette.requests import Request
from starlette.responses import JSONResponse


async def http_exception_handler(
    _request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handles FastAPI HTTPException errors by returning a JSON response with the error detail and status code.

    Args:
        _request (Request): The incoming HTTP request (not used in this handler).
        exc (HTTPException): The HTTPException instance raised during request processing.

    Returns:
        JSONResponse: A response object with the exception's status code and detail message.
    """
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
    )


async def request_validation_exception_handler(
    _request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handles validation errors raised when the request body, query parameters, or path parameters do not conform
    to the expected schema. Returns a 422 Unprocessable Entity response with details about the validation errors.

    Args:
        _request (Request): The incoming HTTP request (not used in this handler).
        exc (RequestValidationError): The validation error instance containing details about the failed validation.

    Returns:
        JSONResponse: A response object with HTTP 422 status and a list of validation errors.
    """
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors()},
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
    )


async def tenant_not_found_exception_handler(
    _request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handles TenantNotFoundError exceptions, typically raised when a requested tenant (e.g., organization or customer)
    cannot be found based on the request context (such as the host header).

    Args:
        _request (Request): The incoming HTTP request (not used in this handler).
        exc (TenantNotFoundError): The exception instance containing information about the missing tenant.

    Returns:
        JSONResponse: A response object with HTTP 404 status and a descriptive error message.
    """
    if isinstance(exc, TenantNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": exc.message}
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
    )


def register_handlers(app: FastAPI) -> FastAPI:
    """
    Registers custom exception handlers for HTTPException, RequestValidationError, and TenantNotFoundError
    with the FastAPI application instance.

    Args:
        app (FastAPI): The FastAPI application to which the exception handlers will be added.

    Returns:
        FastAPI: The same FastAPI application instance, for chaining or further configuration.
    """
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(
        RequestValidationError, request_validation_exception_handler
    )
    app.add_exception_handler(TenantNotFoundError, tenant_not_found_exception_handler)
    return app
