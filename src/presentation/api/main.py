import logging

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
import uvicorn

from aiojobs import Scheduler
from litestar import Litestar
from litestar.middleware import DefineMiddleware
from litestar.types import ASGIApp, Receive, Scope, Send
from uuid6 import uuid7

from src.application.messages.events.message_received import MessageReceived
from src.infrastructure.containers import init_container
from src.infrastructure.log.config import LoggingConfig
from src.infrastructure.log.main import configure_logging
from src.infrastructure.mediator.mediator import MediatorImpl
from src.infrastructure.message_broker.factories import KafkaConnectionFactory
from src.infrastructure.message_broker.interface import MessageBroker
from src.presentation.api.config import APIConfig
from src.presentation.api.controllers import controllers


logger = logging.getLogger(__name__)


def middleware_factory(app: ASGIApp) -> ASGIApp:
    async def my_middleware(scope: Scope, receive: Receive, send: Send) -> None:
        with structlog.contextvars.bound_contextvars(request_id=str(uuid7())):
            await app(scope, receive, send)

    return my_middleware


@asynccontextmanager
async def kafka_connection(app: Litestar) -> AsyncGenerator[None, None]:
    container = init_container()
    broker: KafkaConnectionFactory = container.resolve(MessageBroker)
    await broker.start()
    try:
        yield
    finally:
        await broker.stop()


async def consume_in_background() -> None:
    container = init_container()
    mediator: MediatorImpl = container.resolve(MediatorImpl)
    message_broker: MessageBroker = container.resolve(MessageBroker)

    async for event in message_broker.start_consuming(topic="Message"):
        await mediator.publish(
            [
                MessageReceived(
                    message_id=event.get("message_id"),
                    message_text=event.get("message_text"),
                    chat_id=event.get("chat_id"),
                ),
            ],
        )


@asynccontextmanager
async def background_tasks(app: Litestar) -> AsyncGenerator[None, None]:
    job = await Scheduler().spawn(consume_in_background())
    try:
        yield
    finally:
        await job.close()


def init_api(debug: bool = __debug__, log_cfg: LoggingConfig = LoggingConfig()) -> Litestar:
    logger.debug("Initialize API")
    return Litestar(
        lifespan=[kafka_connection, background_tasks],
        route_handlers=controllers,
        middleware=[DefineMiddleware(middleware_factory)],
        logging_config=configure_logging(cfg=log_cfg),
        debug=debug,
    )


async def run_api(app: Litestar, api_config: APIConfig) -> None:
    config = uvicorn.Config(
        app,
        host=api_config.host,
        port=api_config.port,
        log_level=logging.INFO,
        log_config=None,
    )
    server = uvicorn.Server(config)
    await server.serve()
