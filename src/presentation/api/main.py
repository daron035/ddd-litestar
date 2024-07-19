import uvicorn

from litestar import Litestar

from src.presentation.api.config import APIConfig
from src.presentation.api.controllers.main import get_book, health_check, index


def init_api(debug: bool = __debug__) -> Litestar:
    app = Litestar(route_handlers=[index, get_book, health_check], debug=debug)
    return app


async def run_api(app: Litestar, api_config: APIConfig) -> None:
    config = uvicorn.Config(
        app,
        host=api_config.host,
        port=api_config.port,
    )
    server = uvicorn.Server(config)
    await server.serve()
