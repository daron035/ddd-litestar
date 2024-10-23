import logging

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn

from aiojobs import Scheduler
from fastapi import FastAPI

from src.application.messages.events.message_received import MessageReceived
from src.infrastructure.config import config
from src.infrastructure.containers import init_container
from src.infrastructure.log.main import configure_logging
from src.infrastructure.mediator.mediator import MediatorImpl
from src.infrastructure.message_broker.factories import KafkaConnectionFactory
from src.infrastructure.message_broker.interface import MessageBroker
from src.presentation.api.config import APIConfig
from src.presentation.api.controllers.main import setup_controllers
from src.presentation.api.controllers.responses.orjson import ORJSONResponse
from src.presentation.api.middlewares.main import setup_middlewares


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator:
    container = init_container()
    broker: KafkaConnectionFactory = container.resolve(MessageBroker)
    await broker.start()

    job = await Scheduler().spawn(consume_in_background())
    yield

    await broker.stop()
    await job.close()


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


def init_api() -> FastAPI:
    configure_logging(config.logging)

    logger.debug("Initialize API")
    app = FastAPI(
        # lifespan=lifespan,
        debug=config.api.debug,
        title="User service",
        version="1.0.0",
        default_response_class=ORJSONResponse,
    )
    setup_middlewares(app)
    setup_controllers(app)
    return app


async def run_api(app: FastAPI, api_config: APIConfig) -> None:
    config = uvicorn.Config(
        app,
        host=api_config.host,
        port=api_config.port,
        log_level=logging.INFO,
        log_config=None,
    )
    server = uvicorn.Server(config)
    logger.info("Running API")
    await server.serve()
