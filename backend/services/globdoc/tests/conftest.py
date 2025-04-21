from typing import AsyncGenerator
from pathlib import Path
from dotenv import load_dotenv
import pytest
from httpx import AsyncClient

# Load .env.testing before importing app
env_path = Path(__file__).resolve().parent.parent / ".env.testing"
load_dotenv(dotenv_path=env_path, override=False)

from app import app


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
