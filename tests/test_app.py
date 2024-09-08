import pytest

from litestar import Litestar
from litestar.status_codes import HTTP_200_OK
from litestar.testing import TestClient


def test_index(test_client: TestClient[Litestar]) -> None:
    response = test_client.get("/")
    assert response.status_code == HTTP_200_OK
    assert response.text == "Hello, world!"


def test_get_book(test_client: TestClient[Litestar]) -> None:
    response = test_client.get("/books/1")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"book_id": 1}


@pytest.mark.skip(reason="not implemented")
def test_get_skip():
    assert True


@pytest.mark.xfail()
def test_fail():
    assert False
