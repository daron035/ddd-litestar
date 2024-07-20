from pytest import fixture

from typing import TYPE_CHECKING, AsyncIterator

from litestar import Litestar
from litestar.testing import AsyncTestClient

from src.presentation.api.main import init_api


if TYPE_CHECKING:
    from litestar import Litestar


@fixture
def app() -> Litestar:
    app = init_api()
    # app.dependency_overrides[init_container] = init_dummy_container

    return app


@fixture(scope="function")
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=init_api()) as client:
        yield client
