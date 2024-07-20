from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient

from src.presentation.api.main import init_api


async def test_health_check():
    async with AsyncTestClient(app=init_api()) as client:
        response = await client.get("/healthcheck")
        assert response.status_code == HTTP_200_OK
        assert response.text == "healthy"
