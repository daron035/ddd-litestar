from functools import lru_cache

from punq import Container, Scope
from src.application.common.mediator import Mediator
from src.application.messages.commands.create_chat import CreateChat, CreateChatHandler
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
    def init_mediator() -> Mediator:
        mediator = Mediator()

        mediator.register_command(
            CreateChat,
            [container.resolve(CreateChatHandler)],
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
