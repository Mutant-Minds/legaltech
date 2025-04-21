from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse


async def http_exception_handler(
    _request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handles HTTP exceptions by returning a JSON response with the error message.

    :param _request: The incoming request (unused).
    :param exc: The exception instance.
    :return: JSONResponse with error message and status code.
    """
    if isinstance(exc, HTTPException):
        payload = {"message": exc.detail}
        status_code = exc.status_code
    else:
        # Fallback for unexpected exceptions - you can customize this
        payload = {"message": "Internal server error"}
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return JSONResponse(content=payload, status_code=status_code)


async def request_validation_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    if isinstance(exc, RequestValidationError):
        # your custom handling for validation errors
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors()},
        )
    # fallback for other exceptions if needed
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


def register_handlers(app: FastAPI) -> FastAPI:
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(
        RequestValidationError, request_validation_exception_handler
    )
    return app
