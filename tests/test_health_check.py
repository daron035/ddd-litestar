from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient

from src.presentation.api.main import create_app


async def test_health_check():
    async with AsyncTestClient(app=create_app()) as client:
        response = await client.get("/health-check")
        assert response.status_code == HTTP_200_OK
        assert response.text == "healthy"
