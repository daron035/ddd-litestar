from functools import lru_cache

from punq import Container, Scope

from src.application.messages.commands.create_chat import CreateChat, CreateChatHandler
from src.infrastructure.mediator.mediator import MediatorImpl
from src.infrastructure.repositories.messages.base import BaseChatRepository
from src.infrastructure.repositories.messages.memory import MemoryChatRepository


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(BaseChatRepository, MemoryChatRepository, scope=Scope.singleton)
    container.register(CreateChatHandler)

    # Mediator
    def init_mediator() -> MediatorImpl:
        mediator = MediatorImpl()

        mediator.register_command_handler(CreateChat, CreateChatHandler)

        return mediator

    container.register(MediatorImpl, factory=init_mediator)

    return container
