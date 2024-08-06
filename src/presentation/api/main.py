from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn

from litestar import Litestar

from src.infrastructure.containers import init_container
from src.infrastructure.message_broker.factories import KafkaConnectionFactory
from src.infrastructure.message_broker.interface import MessageBroker
from src.presentation.api.config import APIConfig
from src.presentation.api.controllers.main import create_message, get_book, health_check, index


@asynccontextmanager
async def kafka_connection(app: Litestar) -> AsyncGenerator[None, None]:
    container = init_container()
    broker: KafkaConnectionFactory = container.resolve(MessageBroker)
    await broker.start()
    try:
        yield
    finally:
        await broker.stop()


def init_api(debug: bool = __debug__) -> Litestar:
    app = Litestar(
        lifespan=[kafka_connection],
        route_handlers=[index, get_book, health_check, create_message],
        debug=debug,
    )
    return app


async def run_api(app: Litestar, api_config: APIConfig) -> None:
    config = uvicorn.Config(
        app,
        host=api_config.host,
        port=api_config.port,
    )
    server = uvicorn.Server(config)
    await server.serve()
