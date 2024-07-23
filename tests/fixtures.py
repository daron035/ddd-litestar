from functools import lru_cache

from injector import Binder, Injector, Module, provider, singleton

from src.application.messages.commands.create_chat import CreateChat, CreateChatHandler
from src.application.messages.interfaces.percistence.chat import ChatRepo
from src.infrastructure.mediator.mediator import MediatorImpl
from src.infrastructure.mongo.repositories.memory import MemoryChatRepoImpl


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(ChatRepo, to=MemoryChatRepoImpl, scope=singleton)

    @provider
    def provide_create_chat_handler(self, chat_repository: MemoryChatRepoImpl) -> CreateChatHandler:
        return CreateChatHandler(chat_repository)

    @provider
    def provide_mediator(self, create_chat_handler: CreateChatHandler) -> MediatorImpl:
        mediator = MediatorImpl()
        mediator.register_command_handler(CreateChat, create_chat_handler)
        return mediator


@lru_cache(1)
def init_container() -> Injector:
    return Injector([AppModule])
