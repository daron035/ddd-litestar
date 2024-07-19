import abc

from collections.abc import Awaitable, Callable
from typing import Any, Generic, TypeVar

from src.infrastructure.mediator.interface.entities.command import Command

from .request import Handler


CRes = TypeVar("CRes")
C = TypeVar("C", bound=Command[Any])


class CommandHandler(Handler[C, CRes], abc.ABC, Generic[C, CRes]):
    @abc.abstractmethod
    async def __call__(self, command: C) -> CRes:
        raise NotImplementedError


CommandHandlerType = type[CommandHandler[C, CRes]] | Callable[..., Awaitable[CRes]]
