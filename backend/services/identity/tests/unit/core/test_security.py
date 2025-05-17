from datetime import datetime, timedelta

import pytest
from core import security
from core.config import settings
from jose import jwt


@pytest.mark.asyncio
async def test_create_access_token_contains_expected_fields() -> None:
    """
    Test that create_access_token returns a JWT token containing expected payload fields.
    """
    subject = "user123"
    claims = {"role": "admin"}

    token = security.create_access_token(subject=subject, claims=claims)
    assert isinstance(token, str)

    # Decode without verification to inspect payload
    payload = jwt.get_unverified_claims(token)

    assert payload["sub"] == subject
    assert payload["aud"] == "account"
    assert "exp" in payload
    assert "claims" in payload
    assert payload["claims"] == claims

    # exp should be roughly now + configured expiration
    exp = datetime.fromtimestamp(payload["exp"])
    expected_exp = datetime.now() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    # Allow a small delta for execution time
    assert abs((exp - expected_exp).total_seconds()) < 5


@pytest.mark.asyncio
async def test_create_access_token_without_claims() -> None:
    """
    Test that create_access_token works correctly when no claims are provided.
    """
    subject = "user456"

    token = security.create_access_token(subject=subject, claims=None)
    payload = jwt.get_unverified_claims(token)

    assert payload["sub"] == subject
    assert "claims" not in payload


def test_verify_password_valid_and_invalid() -> None:
    """
    Test verify_password returns True for correct password and False otherwise.
    """
    raw_password = "mysecretpassword"
    hashed_password = security.get_password_hash(raw_password)

    # Correct password
    assert security.verify_password(raw_password, hashed_password) is True

    # Incorrect password
    assert security.verify_password("wrongpassword", hashed_password) is False


def test_get_password_hash_returns_string() -> None:
    """
    Test get_password_hash returns a string hash for a plaintext password.
    """
    raw_password = "anotherpassword"
    hashed = security.get_password_hash(raw_password)

    assert isinstance(hashed, str)
    # The hashed password should not be the same as the raw password
    assert hashed != raw_password

    # Verify the hash matches the original password
    assert security.verify_password(raw_password, hashed) is True
