from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
@patch(
    "api.v1.endpoints.register.security.get_password_hash", return_value="mocked-hash"
)
@patch("api.v1.endpoints.register.crud.account_user.create", new_callable=AsyncMock)
@patch(
    "api.v1.endpoints.register.crud.account_user.get_by_email", new_callable=AsyncMock
)
@patch("api.v1.endpoints.register.schemas.AccountUserCreate")
async def test_successful_registration(
    mock_account_user_create: MagicMock,
    mock_get_by_email: AsyncMock,
    mock_create: AsyncMock,
    mock_hash: MagicMock,
    async_client: AsyncClient,
) -> None:
    """
    Test case: Successful registration

    Simulates creating a new user when the email does not exist.
    Expects HTTP 201 Created with success message.
    """
    mock_get_by_email.return_value = None
    mock_create.return_value = None
    mock_account_user_create.return_value = MagicMock()

    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "securepassword123",
        "username": "testuser",
        "country_code": "+91",
        "phone": "1234567890",
    }

    response = await async_client.post("/api/v1/register", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"message": "Registration successful!"}


@pytest.mark.asyncio
@patch("specter.crud.account_user.get_by_email", new_callable=AsyncMock)
async def test_registration_email_already_exists(
    mock_get_by_email: AsyncMock,
    async_client: AsyncClient,
) -> None:
    """
    Test case: Email already exists

    Simulates user registration attempt with an email that already exists.
    Expects HTTP 400 Bad Request with appropriate error detail.
    """
    mock_get_by_email.return_value = object()  # Any non-None value

    payload = {
        "name": "Test User",
        "email": "duplicate@example.com",
        "password": "irrelevant",
        "username": "dupuser",
        "country_code": "+1",
        "phone": "9999999999",
    }

    response = await async_client.post("/api/v1/register", json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Invalid emailId. Reason - Already exists!"


@pytest.mark.asyncio
@patch("specter.crud.account_user.get_by_email", side_effect=Exception("DB crashed"))
async def test_registration_internal_server_error(
    mock_get_by_email: AsyncMock,
    async_client: AsyncClient,
) -> None:
    """
    Test case: Internal server error

    Simulates a failure in the DB lookup (e.g., database crash).
    Expects HTTP 500 Internal Server Error with appropriate error detail.
    """
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "securepassword123",
        "username": "testuser",
        "country_code": "+91",
        "phone": "1234567890",
    }

    response = await async_client.post("/api/v1/register", json=payload)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["detail"].startswith("Request failed:")
