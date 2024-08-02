from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope

from src.application.messages.commands.create_chat import CreateChat, CreateChatHandler
from src.application.messages.interfaces.percistence.chat import ChatRepo
from src.domain.common.events.event import Event
from src.infrastructure.event_bus.event_handler import EventHandlerPublisher
from src.infrastructure.mediator.mediator import MediatorImpl
from src.infrastructure.mongo.repositories.chat import MongoDBChatRepoImpl
from src.presentation.api.config import Config


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    # Mediator
    def init_mediator() -> MediatorImpl:
        mediator = MediatorImpl()
        # mediator. EventObserverImpl

        create_chat_handler = CreateChatHandler(
            chat_repository=container.resolve(ChatRepo),
            _mediator=mediator,
        )

        mediator.register_command_handler(CreateChat, create_chat_handler)
        mediator.register_event_handler(Event, EventHandlerPublisher)

        return mediator

    def init_chat_mongodb_repository():
        config: Config = container.resolve(Config)
        client = AsyncIOMotorClient(config.mongo.mongodb_connection_uri, serverSelectionTimeoutMS=3000)
        return MongoDBChatRepoImpl(
            mongo_client=client,
            mongo_db_name=config.mongo.mongodb_chat_database,
            mongo_collection_name=config.mongo.mongodb_chat_collection,
        )

    container.register(ChatRepo, factory=init_chat_mongodb_repository, scope=Scope.singleton)
    container.register(MediatorImpl, factory=init_mediator)

    return container
