from pytest import fixture

from typing import TYPE_CHECKING, AsyncIterator

from litestar import Litestar
from litestar.testing import AsyncTestClient

from src.presentation.api.main import create_app

if TYPE_CHECKING:
    from litestar import Litestar


@fixture
def app() -> Litestar:
    app = create_app()
    # app.dependency_overrides[init_container] = init_dummy_container

    return app


@fixture(scope="function")
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=create_app()) as client:
        yield client
