from fastapi.testclient import TestClient
import pytest


async def test_health_check(
    client: TestClient,
) -> None:
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.text == "healthy"


async def test_get_book(
    client: TestClient,
) -> None:
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json() == {"book_id": 1}


@pytest.mark.skip(reason="not implemented")
def test_get_skip():
    assert True


@pytest.mark.xfail()
def test_fail():
    assert False
