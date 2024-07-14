import pytest

from litestar import Litestar
from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient


async def test_health_check_with_fixture(test_client: AsyncTestClient[Litestar]) -> None:
    response = await test_client.get("/health-check")
    assert response.status_code == HTTP_200_OK
    assert response.text == "healthy"


async def test_get_book(test_client: AsyncTestClient[Litestar]) -> None:
    response = await test_client.get("/books/1")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"book_id": 1}


@pytest.mark.skip(reason="not implemented")
def test_get_skip():
    assert True


@pytest.mark.xfail()
def test_fail():
    assert False
