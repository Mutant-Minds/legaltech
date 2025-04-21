from pathlib import Path
from typing import AsyncGenerator

import pytest
from dotenv import load_dotenv
from httpx import AsyncClient

load_dotenv(dotenv_path=Path(__file__).parent / ".env.test", override=True)

from app import app  # noqa: E402


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Provides an AsyncClient instance for testing FastAPI app endpoints.
    """
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
