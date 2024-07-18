from functools import lru_cache

from injector import Binder, Injector, Module, provider, singleton

from src.application.messages.commands.create_chat import CreateChat, CreateChatHandler
from src.infrastructure.mediator.mediator import MediatorImpl
from src.infrastructure.repositories.messages.base import BaseChatRepository
from src.infrastructure.repositories.messages.memory import MemoryChatRepository


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(BaseChatRepository, to=MemoryChatRepository, scope=singleton)

    @provider
    def provide_create_chat_handler(self, chat_repository: BaseChatRepository) -> CreateChatHandler:
        return CreateChatHandler(chat_repository)

    @provider
    def provide_mediator(self, create_chat_handler: CreateChatHandler) -> MediatorImpl:
        mediator = MediatorImpl()
        mediator.register_command_handler(CreateChat, create_chat_handler)
        return mediator


@lru_cache(1)
def init_container() -> Injector:
    return Injector([AppModule])
