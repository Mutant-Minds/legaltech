import schemas
from core import security
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from specter import crud
from specter.db.session import get_shared_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    "/login",
    summary="Generate Access Token to support User Login",
    response_model=schemas.Token,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "User authenticated successfully. Returns access token.",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
                        "token_type": "bearer",
                    }
                }
            },
        },
        401: {
            "description": "Authentication failed due to incorrect password",
            "content": {
                "application/json": {
                    "example": {"detail": "Incorrect password provided"}
                }
            },
        },
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid emailId. Reason - Does not exist!"}
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
async def login(
    request: Request,
    *,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_shared_db),
) -> schemas.Token:
    """
    Authenticate a user and generate an access token.

    This endpoint validates the user's credentials (email/username and password), and if valid,
    returns a JWT access token that can be used for authenticated requests. The credentials
    are checked against the records in the `public.account_user` table.

    Args:
        request (Request): FastAPI request context.
        form_data (OAuth2PasswordRequestForm): Form data containing username and password.
        db (AsyncSession): Shared asynchronous database session.

    Returns:
        JSONResponse: A response containing the access token and token type with HTTP 200 status.
    """
    try:
        account = await crud.account_user.get_by_email(db=db, email=form_data.username)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid emailId. Reason - Does not exist!",
            )

        if not security.verify_password(
            plain_password=form_data.password, hashed_password=account.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password provided",
            )

        return schemas.Token(
            access_token=security.create_access_token(
                subject=account.id,
                claims={"name": account.name, "email": account.email},
            ),
            token_type=schemas.TokenType.BEARER,
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Request failed: {str(e)}",
        )
