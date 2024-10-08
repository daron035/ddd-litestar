from collections.abc import Sequence
from typing import Any, Generic, Protocol, TypeVar

from src.infrastructure.mediator.interface.entities.event import Event
from src.infrastructure.mediator.interface.handlers.event import EventHandlerType
from src.infrastructure.mediator.middlewares.base import MiddlewareType


Self = TypeVar("Self", bound="EventObserver")
E = TypeVar("E", bound=Event)


class Listener(Generic[E]):
    def __init__(self, event: type[E], handler: EventHandlerType[E]):
        self._event = event
        self._handler = handler

    def is_listen(self, event: Event) -> bool:
        return isinstance(event, self._event)

    @property
    def event(self) -> type[E]:
        return self._event

    @property
    def handler(self) -> EventHandlerType[E]:
        return self._handler


class EventObserver(Protocol):
    @property
    def listeners(self) -> tuple[Listener[Any], ...]:
        raise NotImplementedError

    @property
    def middlewares(self) -> tuple[MiddlewareType[Event, Any], ...]:
        raise NotImplementedError

    def copy(self: Self) -> Self:
        raise NotImplementedError

    def register_listener(self, listener: Listener[Any]) -> None:
        raise NotImplementedError

    async def publish(self, events: Sequence[Event], *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError
