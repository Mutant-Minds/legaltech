from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union, cast

from core.config import settings
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any],
    claims: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Creates a JSON Web Token (JWT) for the given subject (usually a user identifier).

    The token includes an expiration time and optional user-specific claims. It is signed
    using the application's secret key and is intended for authentication purposes.

    Args:
        subject (Union[str, Any]): Identifier for the token subject, typically a user ID or email.
        claims (Optional[Dict]): Additional claims to include in the token payload.

    Returns:
        str: Encoded JWT access token.
    """
    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": str(subject), "aud": "account"}
    if claims:
        to_encode.update({"claims": claims})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies whether a plaintext password matches its hashed counterpart.

    Uses the configured password hashing context to perform secure comparison.

    Args:
        plain_password (str): The raw password input provided by the user.
        hashed_password (str): The stored, hashed password to compare against.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    return cast(bool, pwd_context.verify(plain_password, hashed_password))


def get_password_hash(password: str) -> str:
    """
    Hashes a plaintext password using the application's password hashing context.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        str: A securely hashed password suitable for storage.
    """
    return cast(str, pwd_context.hash(password))
