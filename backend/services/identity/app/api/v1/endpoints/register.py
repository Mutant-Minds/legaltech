import schemas
from core import security
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from specter import crud
from specter.db.session import get_shared_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    "/register",
    summary="Register a User",
    response_model=schemas.Msg,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "User registered successfully",
            "content": {
                "application/json": {"example": {"message": "Registration successful"}}
            },
        },
        400: {
            "description": "Invalid request (e.g., emailId already exists)",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid emailId. Reason - Already exists!"}
                }
            },
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": "Request failed: Unknown error"}
                }
            },
        },
    },
)
async def register(
    request: Request,
    *,
    register_in: schemas.RegisterUser,
    db: AsyncSession = Depends(get_shared_db),
) -> JSONResponse:
    """
    Register a new user (AccountUser) into the system.

    This endpoint checks for email uniqueness, hashes the password, generates the default username if not provided,
    and creates the user in the database (public.account_user).

    Args:
        request (Request): FastAPI request context.
        register_in (schemas.RegisterUser): Input schema for user registration.
        db (AsyncSession): Shared DB session.

    Returns:
        JSONResponse: Confirmation message with status code 201.
    """
    try:
        account = await crud.account_user.get_by_email(db=db, email=register_in.email)
        if account:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid emailId. Reason - Already exists!",
            )
        await crud.account_user.create(
            db=db,
            obj_in=schemas.AccountUserCreate(
                name=register_in.name,
                email=register_in.email,
                username=register_in.username,
                password_hash=security.get_password_hash(password=register_in.password),
                country_code=register_in.country_code,
                phone=register_in.phone,
            ),
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=jsonable_encoder(schemas.Msg(message="Registration successful!")),
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Request failed: {str(e)}",
        )
