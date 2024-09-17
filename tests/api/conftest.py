from collections.abc import AsyncIterator
from typing import TYPE_CHECKING

from litestar import Litestar
from litestar.testing import AsyncTestClient
from pytest import fixture

from src.presentation.api.controllers import controllers
from src.presentation.api.main import init_api


if TYPE_CHECKING:
    from litestar import Litestar


# @fixture()
def app() -> Litestar:
    return Litestar(
        route_handlers=controllers,
    )


@fixture(scope="function")
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=app()) as client:
        yield client
