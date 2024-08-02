from collections.abc import Awaitable, Callable, Sequence
from typing import Any, TypeVar

from src.infrastructure.mediator.dispatchers.request import DEFAULT_MIDDLEWARES
from src.infrastructure.mediator.interface.entities.event import Event
from src.infrastructure.mediator.interface.handlers.event import EventHandlerType
from src.infrastructure.mediator.interface.observers.event import EventObserver, Listener
from src.infrastructure.mediator.middlewares.base import MiddlewareType, wrap_middleware


Self = TypeVar("Self", bound="EventObserverImpl")
E = TypeVar("E", bound=Event)
Middlewares = Sequence[MiddlewareType[Event, Any]]


class EventObserverImpl(EventObserver):
    def __init__(
        self,
        middlewares: Middlewares = (),
        *,
        listeners: list[Listener[Event]] | None = None,
    ) -> None:
        self._middlewares: Middlewares = middlewares

        if listeners is None:
            listeners = []
        self._listeners = listeners

    @property
    def listeners(self) -> tuple[Listener[Event], ...]:
        return tuple(self._listeners)

    @property
    def middlewares(self) -> tuple[MiddlewareType[Event, Any], ...]:
        return tuple(self._middlewares)

    def copy(self: Self) -> Self:
        return self.__class__(self._middlewares, listeners=self._listeners)

    def register_listener(self, listener: Listener[Event]) -> None:
        self._listeners.append(listener)
        print(f"Listener registered: {self._listeners}")

    async def publish(self, events: Sequence[Event], *args: Any, **kwargs: Any) -> None:
        print(f"Publishing events: {events}")
        print(f"Current listeners before handling: {self._listeners}")
        await self._handle(events, *args, **kwargs)

    async def _handle(self, events: Sequence[Event], *args: Any, **kwargs: Any) -> None:
        middlewares: Middlewares = self._middlewares if self._middlewares else DEFAULT_MIDDLEWARES

        for event in events:
            print(f"Handling event: {event}")
            print(f"Listeners: {self._listeners}")
            for listener in self._listeners:
                wrapped_handler = self._wrap_middleware(middlewares, listener.handler)
                await wrapped_handler(event, *args, **kwargs)

    @staticmethod
    def _wrap_middleware(
        middlewares: Middlewares,
        handler: EventHandlerType[E],
    ) -> Callable[..., Awaitable[Any]]:
        return wrap_middleware(middlewares, handler)
