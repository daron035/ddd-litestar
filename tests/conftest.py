import pytest
from litestar import Litestar
from litestar.testing import TestClient

from collections.abc import Iterator
from typing import TYPE_CHECKING

from src.presentation.api.main import app

if TYPE_CHECKING:
    from litestar import Litestar


@pytest.fixture(scope="function")
def test_client() -> Iterator[TestClient[Litestar]]:
    with TestClient(app=app) as client:
        yield client
