import logging

from functools import lru_cache
from uuid import uuid4

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope

from src.application.common.interfaces.uow import UnitOfWork
from src.application.messages.commands.create_chat import CreateChat, CreateChatHandler
from src.application.messages.commands.create_message import CreateMessage, CreateMessageHandler
from src.application.messages.events.message_received import MessageReceived, MessageReceivedHandler
from src.application.messages.interfaces.percistence.chat import ChatRepo
from src.application.messages.interfaces.percistence.message import MessageRepo
from src.application.messages.interfaces.percistence.reader import MessageReader
from src.application.messages.queries.get_messages_by_chat import GetMessagesByChatId, GetMessagesByChatIdHandler
from src.application.messages.websockets.managers import ConnectionManager, WebSocketConnectionManager
from src.application.user.commands.create_user import CreateUser, CreateUserHandler
from src.application.user.interfaces.persistence import UserReader, UserRepo
from src.application.user.interfaces.persistence.repo import UserRepo
from src.application.user.queries.get_user_by_id import GetUserById, GetUserByIdHandler
from src.domain.common.events.event import Event
from src.infrastructure.config_loader import load_config
from src.infrastructure.event_bus.event_bus import EventBusImpl
from src.infrastructure.event_bus.event_handler import EventHandlerPublisher
from src.infrastructure.log.event_handler import EventLogger
from src.infrastructure.mediator.dispatchers.command import CommandDispatcherImpl
from src.infrastructure.mediator.dispatchers.query import QueryDispatcherImpl
from src.infrastructure.mediator.mediator import MediatorImpl
from src.infrastructure.mediator.middlewares.logging import LoggingMiddleware
from src.infrastructure.mediator.observers.event import EventObserverImpl
from src.infrastructure.message_broker.config import EventBusConfig
from src.infrastructure.message_broker.interface import MessageBroker
from src.infrastructure.message_broker.kafka import KafkaMessageBroker
from src.infrastructure.mongo.config import MongoConfig
from src.infrastructure.mongo.repositories.chat import MongoDBChatRepoImpl
from src.infrastructure.mongo.repositories.message import MongoDBMessageReaderImpl, MongoDBMessageRepoImpl
from src.infrastructure.postgres.main import PostgresManager
from src.infrastructure.postgres.repositories.user import UserReaderImpl, UserRepoImpl
from src.infrastructure.postgres.services.healthcheck import PgHealthCheck, PostgresHealthcheckService
from src.infrastructure.postgres.uow import SQLAlchemyUoW
from src.infrastructure.uow import build_uow
from src.presentation.api.config import Config


@lru_cache(maxsize=1)
def init_container() -> Container:
    _config = load_config(Config)
    container = Container()

    register_brokers(container, _config)
    register_repositories(container, _config)
    register_mediator(container)
    _db_factories(container, _config)

    return container


def register_brokers(container: Container, config: Config) -> None:
    container.register(MessageBroker, factory=lambda: _init_kafka(config.event_bus), scope=Scope.singleton)
    container.register(EventBusImpl, factory=lambda: _init_event_bus(container), scope=Scope.singleton)


def register_repositories(container: Container, config: Config) -> None:
    container.register(ChatRepo, factory=lambda: _init_chat_mongodb_repository(config), scope=Scope.singleton)
    container.register(MessageRepo, factory=lambda: _init_message_mongodb_repository(config), scope=Scope.singleton)
    container.register(MessageReader, factory=lambda: _init_message_mongodb_reader(config), scope=Scope.singleton)
    container.register(WebSocketConnectionManager, instance=ConnectionManager(), scope=Scope.singleton)


def register_mediator(container: Container) -> None:
    container.register(MediatorImpl, factory=lambda: _init_mediator(container))


def _init_mediator(container: Container) -> MediatorImpl:
    middlewares = (LoggingMiddleware("mediator", level=logging.INFO),)
    command_dispatcher = CommandDispatcherImpl(middlewares=middlewares)
    query_dispatcher = QueryDispatcherImpl(middlewares=middlewares)
    event_observer = EventObserverImpl(middlewares=middlewares)
    mediator = MediatorImpl(command_dispatcher, query_dispatcher, event_observer)

    create_chat_handler = CreateChatHandler(
        chat_repository=container.resolve(ChatRepo),
        mediator=mediator,
    )
    create_message_handler = CreateMessageHandler(
        chat_repository=container.resolve(ChatRepo),
        message_repository=container.resolve(MessageRepo),
        mediator=mediator,
    )
    create_user_handler = CreateUserHandler(
        user_repo=container.resolve(UserRepo),
        uow=container.resolve(UnitOfWork),
        mediator=mediator,
    )

    mediator.register_command_handler(CreateChat, create_chat_handler)
    mediator.register_command_handler(CreateMessage, create_message_handler)
    mediator.register_command_handler(CreateUser, create_user_handler)

    get_chat_messages_handler = GetMessagesByChatIdHandler(
        messages_repository=container.resolve(MessageReader),
    )
    get_user_by_id_handler = GetUserByIdHandler(
        user_reader=container.resolve(UserReader),
    )

    mediator.register_query_handler(GetMessagesByChatId, get_chat_messages_handler)
    mediator.register_query_handler(GetUserById, get_user_by_id_handler)

    mediator.register_event_handler(Event, _init_event_handler(container))
    mediator.register_event_handler(Event, EventLogger)
    mediator.register_event_handler(MessageReceived, _init_message_received_handler(container))

    return mediator


def _init_event_bus(container: Container) -> EventBusImpl:
    message_broker: MessageBroker = container.resolve(MessageBroker)
    return EventBusImpl(_message_broker=message_broker)


def _init_event_handler(container: Container) -> EventHandlerPublisher:
    event_bus: EventBusImpl = container.resolve(EventBusImpl)
    return EventHandlerPublisher(_event_bus=event_bus)


def _init_message_received_handler(container: Container) -> MessageReceivedHandler:
    ws_manager: WebSocketConnectionManager = container.resolve(WebSocketConnectionManager)
    return MessageReceivedHandler(_ws_manager=ws_manager)


def _init_chat_mongodb_repository(config: Config) -> MongoDBChatRepoImpl:
    client = _create_mongo_client(config.mongo)
    return MongoDBChatRepoImpl(
        mongo_client=client,
        mongo_db_name=config.mongo.mongodb_chat_database,
        mongo_collection_name=config.mongo.mongodb_chat_collection,
    )


def _init_message_mongodb_repository(config: Config) -> MongoDBMessageRepoImpl:
    client = _create_mongo_client(config.mongo)
    return MongoDBMessageRepoImpl(
        mongo_client=client,
        mongo_db_name=config.mongo.mongodb_chat_database,
        mongo_collection_name=config.mongo.mongodb_chat_collection,
    )


def _init_message_mongodb_reader(config: Config) -> MongoDBMessageReaderImpl:
    client = _create_mongo_client(config.mongo)
    return MongoDBMessageReaderImpl(
        mongo_client=client,
        mongo_db_name=config.mongo.mongodb_chat_database,
        mongo_collection_name=config.mongo.mongodb_chat_collection,
    )


def _create_mongo_client(mongo_config: MongoConfig) -> AsyncIOMotorClient:
    return AsyncIOMotorClient(mongo_config.mongodb_connection_uri, serverSelectionTimeoutMS=3000)


def _init_kafka(event_bus_config: EventBusConfig) -> KafkaMessageBroker:
    _producer = AIOKafkaProducer(bootstrap_servers=event_bus_config.bootstrap_servers)
    _consumer = AIOKafkaConsumer(
        bootstrap_servers=event_bus_config.bootstrap_servers,
        group_id=f"chats-{uuid4()}",
        metadata_max_age_ms=30000,
    )
    return KafkaMessageBroker(producer=_producer, consumer=_consumer)


def _db_factories(container: Container, config: Config) -> None:
    container.register(PostgresManager, factory=lambda: PostgresManager(config.postgres_db), scope=Scope.singleton)
    psql: PostgresManager = container.resolve(PostgresManager)
    session = psql.session_factory()
    read_only_session = psql.read_only_session_factory()
    container.register(PgHealthCheck, factory=lambda: PostgresHealthcheckService(session))

    container.register(UnitOfWork, factory=lambda: build_uow(SQLAlchemyUoW(session)))
    container.register(UserRepo, factory=lambda: UserRepoImpl(session))
    container.register(UserReader, factory=lambda: UserReaderImpl(read_only_session))
