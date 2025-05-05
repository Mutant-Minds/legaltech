from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from main import app


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Provides an AsyncClient instance for testing FastAPI app endpoints.
    """
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
