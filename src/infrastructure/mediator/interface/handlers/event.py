import abc

from collections.abc import Awaitable, Callable
from typing import Any, Generic, TypeVar

from src.infrastructure.mediator.interface.entities.event import Event

from .request import Handler


E = TypeVar("E", bound=Event)


class EventHandler(Handler[E, Any], abc.ABC, Generic[E]):
    @abc.abstractmethod
    async def __call__(self, event: E) -> Any:
        raise NotImplementedError


EventHandlerType = type[EventHandler[E]] | Callable[..., Awaitable[Any]]
