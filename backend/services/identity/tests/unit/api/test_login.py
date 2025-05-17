from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
import schemas
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
@patch("specter.crud.account_user.get_by_email", new_callable=AsyncMock)
@patch("core.security.verify_password", return_value=True)
@patch("core.security.create_access_token", return_value="mocked-token")
async def test_successful_login(
    mock_create_token: Any,
    mock_verify_password: Any,
    mock_get_by_email: AsyncMock,
    async_client: AsyncClient,
) -> None:
    """
    Test case: Successful login

    Simulates a valid user login scenario with correct email and password,
    returning a 200 status code and a JWT access token.
    """
    mock_get_by_email.return_value = type(
        "User",
        (),
        {
            "id": "user123",
            "name": "Jane Doe",
            "email": "jane@example.com",
            "password_hash": "hashed",
        },
    )()

    response = await async_client.post(
        "/api/v1/login",
        data={"username": "jane@example.com", "password": "correctpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "mocked-token",
        "token_type": schemas.TokenType.BEARER.value,
    }


@pytest.mark.asyncio
@patch("specter.crud.account_user.get_by_email")
async def test_user_not_found(
    mock_get_by_email: AsyncMock, async_client: AsyncClient
) -> None:
    """
    Test case: User not found

    Simulates login attempt with an email that does not exist,
    expecting a 404 Not Found with appropriate error detail.
    """
    mock_get_by_email.return_value = None

    response = await async_client.post(
        "/api/v1/login",
        data={"username": "unknown@example.com", "password": "any-password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Invalid emailId. Reason - Does not exist!"


@pytest.mark.asyncio
@patch("specter.crud.account_user.get_by_email", new_callable=AsyncMock)
@patch("core.security.verify_password", return_value=False)
async def test_incorrect_password(
    mock_verify_password: Any,
    mock_get_by_email: AsyncMock,
    async_client: AsyncClient,
) -> None:
    """
    Test case: Incorrect password

    Simulates a login attempt with a valid user but incorrect password,
    expecting a 401 Unauthorized with appropriate error detail.
    """
    mock_get_by_email.return_value = type(
        "User",
        (),
        {
            "id": "user123",
            "name": "Jane Doe",
            "email": "jane@example.com",
            "password_hash": "hashed",
        },
    )()

    response = await async_client.post(
        "/api/v1/login",
        data={"username": "jane@example.com", "password": "wrongpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect password provided"


@pytest.mark.asyncio
@patch("specter.crud.account_user.get_by_email")
async def test_internal_server_error(
    mock_get_by_email: AsyncMock,
    async_client: AsyncClient,
) -> None:
    """
    Test case: Internal server error

    Simulates an unexpected server-side error (e.g., DB connection issue),
    expecting a 500 Internal Server Error with appropriate detail.
    """
    mock_get_by_email.side_effect = Exception("Database error")

    response = await async_client.post(
        "/api/v1/login",
        data={"username": "test@example.com", "password": "irrelevant"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Request failed" in response.json()["detail"]
