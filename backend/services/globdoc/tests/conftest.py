from pathlib import Path
from typing import AsyncGenerator

import pytest
from dotenv import load_dotenv
from httpx import AsyncClient

from app import app

# Load .env.testing before importing app
env_path = Path(__file__).resolve().parent.parent / ".env.testing"
load_dotenv(dotenv_path=env_path, override=False)


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
