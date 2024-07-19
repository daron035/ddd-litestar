from collections.abc import Sequence
from typing import Any, TypeVar

from src.infrastructure.mediator.dispatchers.command import CommandDispatcherImpl
from src.infrastructure.mediator.dispatchers.query import QueryDispatcherImpl
from src.infrastructure.mediator.interface.dispatchers.command import CommandDispatcher
from src.infrastructure.mediator.interface.dispatchers.query import QueryDispatcher
from src.infrastructure.mediator.interface.entities import Command, Event, Query
from src.infrastructure.mediator.interface.handlers.command import CommandHandlerType
from src.infrastructure.mediator.interface.handlers.event import EventHandlerType
from src.infrastructure.mediator.interface.handlers.query import QueryHandlerType
from src.infrastructure.mediator.interface.mediator import Mediator
from src.infrastructure.mediator.interface.observers.event import EventObserver, Listener
from src.infrastructure.mediator.observers.event import EventObserverImpl


C = TypeVar("C", bound=Command[Any])
CRes = TypeVar("CRes")
Q = TypeVar("Q", bound=Query[Any])
QRes = TypeVar("QRes")
E = TypeVar("E", bound=Event)


class MediatorImpl(Mediator):
    def __init__(
        self,
        command_dispatcher: CommandDispatcher | None = None,
        query_dispatcher: QueryDispatcher | None = None,
        event_observer: EventObserver | None = None,
        *,
        extra_data: dict[str, Any] | None = None,
    ):
        if command_dispatcher is None:
            command_dispatcher = CommandDispatcherImpl()
        if query_dispatcher is None:
            query_dispatcher = QueryDispatcherImpl()
        if event_observer is None:
            event_observer = EventObserverImpl()

        self._command_dispatcher = command_dispatcher
        self._query_dispatcher = query_dispatcher
        self._event_observer = event_observer
        self._extra_data = extra_data if extra_data is not None else {}

    @property
    def extra_data(self) -> dict[str, Any]:
        return self._extra_data

    def bind(self, **extra_data: Any) -> None:
        pass

    def unbind(self, *keys: str) -> None:
        pass

    def register_command_handler(self, command: type[C], handler: CommandHandlerType[C, CRes]) -> None:
        self._command_dispatcher.register_handler(command, handler)

    def register_query_handler(self, query: type[Q], handler: QueryHandlerType[Q, QRes]) -> None:
        self._query_dispatcher.register_handler(query, handler)

    def register_event_handler(self, event: type[E], handler: EventHandlerType[E]) -> None:
        listener = Listener(event, handler)
        self._event_observer.register_listener(listener)

    async def send(self, command: Command[CRes], *args: Any, **kwargs: Any) -> CRes:
        kwargs = self._extra_data | kwargs
        return await self._command_dispatcher.send(command, *args, **kwargs)

    async def query(self, query: Query[QRes], *args: Any, **kwargs: Any) -> QRes:
        kwargs = self._extra_data | kwargs
        return await self._query_dispatcher.query(query, *args, **kwargs)

    async def publish(self, events: Event | Sequence[Event], *args: Any, **kwargs: Any) -> None:
        if isinstance(events, Event):
            events = (events,)
        kwargs = self._extra_data | kwargs
        await self._event_observer.publish(events, *args, **kwargs)
