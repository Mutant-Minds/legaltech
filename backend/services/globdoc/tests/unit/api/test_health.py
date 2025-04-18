from http import HTTPStatus
import pytest
import schemas


@pytest.mark.asyncio
async def test_health_probe(async_client):
    """

    Args:
        async_client:

    Returns:

    """
    response = await async_client.get("/health/")
    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert data["status"] == schemas.HealthStatus.OK.value
    assert isinstance(data["service"], str)
    assert data["dependencies"] is None
