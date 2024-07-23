from functools import lru_cache

from injector import Binder, Injector, Module, provider, singleton
from motor.motor_asyncio import AsyncIOMotorClient

from src.application.messages.commands.create_chat import CreateChat, CreateChatHandler
from src.application.messages.commands.create_message import CreateMessage, CreateMessageHandler
from src.application.messages.interfaces.percistence.chat import ChatRepo
from src.application.messages.interfaces.percistence.message import MessageRepo
from src.infrastructure.mediator.interface.mediator import EventMediator
from src.infrastructure.mediator.mediator import MediatorImpl
from src.infrastructure.mongo.repositories.chat import MongoDBChatRepoImpl
from src.infrastructure.mongo.repositories.message import MongoDBMessageRepoImpl
from src.presentation.api.config import Config


class RepositoryModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(Config, to=Config(), scope=singleton)

    @singleton
    @provider
    def provide_mongo_client(self, config: Config) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(config.mongo.mongodb_connection_uri, serverSelectionTimeoutMS=3000)

    @singleton
    @provider
    def provide_chat_repo(self, config: Config, client: AsyncIOMotorClient) -> ChatRepo:
        return MongoDBChatRepoImpl(
            mongo_client=client,
            mongo_db_name=config.mongo.mongodb_chat_database,
            mongo_collection_name=config.mongo.mongodb_chat_collection,
        )

    @singleton
    @provider
    def provide_message_repo(self, config: Config, client: AsyncIOMotorClient) -> MessageRepo:
        return MongoDBMessageRepoImpl(
            mongo_client=client,
            mongo_db_name=config.mongo.mongodb_chat_database,
            mongo_collection_name=config.mongo.mongodb_chat_collection,
        )


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        # binder.bind(ChatRepo, to=MemoryChatRepoImpl, scope=singleton)  # noqa: ERA001
        # binder.bind(MessageRepo, to=MongoDBChatRepoImpl, scope=singlet
        binder.bind(EventMediator, to=MediatorImpl, scope=singleton)

    @provider
    def provide_create_chat_handler(self, chat_repository: ChatRepo) -> CreateChatHandler:
        return CreateChatHandler(chat_repository)

    @provider
    def provide_create_message_handler(
        self,
        chat_repository: ChatRepo,
        message_repository: MessageRepo,
        _mediator: EventMediator,
    ) -> CreateMessageHandler:
        return CreateMessageHandler(chat_repository, message_repository, _mediator)

    @provider
    def provide_mediator(
        self,
        create_chat_handler: CreateChatHandler,
        create_message_handler: CreateMessageHandler,
    ) -> MediatorImpl:
        mediator = MediatorImpl()
        mediator.register_command_handler(CreateChat, create_chat_handler)
        mediator.register_command_handler(CreateMessage, create_message_handler)
        return mediator


@lru_cache(1)
def init_container() -> Injector:
    return Injector([AppModule, RepositoryModule])
