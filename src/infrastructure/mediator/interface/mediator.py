from collections.abc import Sequence
from typing import Any, Protocol, TypeVar

from src.infrastructure.mediator.interface.entities.command import Command
from src.infrastructure.mediator.interface.entities.event import Event
from src.infrastructure.mediator.interface.entities.query import Query
from src.infrastructure.mediator.interface.handlers.command import CommandHandlerType
from src.infrastructure.mediator.interface.handlers.event import EventHandlerType
from src.infrastructure.mediator.interface.handlers.query import QueryHandlerType


Self = TypeVar("Self", bound="BaseMediator")
C = TypeVar("C", bound=Command[Any])
CRes = TypeVar("CRes")
Q = TypeVar("Q", bound=Query[Any])
QRes = TypeVar("QRes")
E = TypeVar("E", bound=Event)


class BaseMediator(Protocol):
    @property
    def extra_data(self) -> dict[str, Any]:
        raise NotImplementedError


class CommandMediator(BaseMediator, Protocol):
    async def send(self, command: Command[CRes], *args: Any, **kwargs: Any) -> CRes:
        raise NotImplementedError

    def register_command_handler(self, command: type[C], handler: CommandHandlerType[C, CRes]) -> None:
        raise NotImplementedError


class QueryMediator(BaseMediator, Protocol):
    async def query(self, query: Query[QRes], *args: Any, **kwargs: Any) -> QRes:
        raise NotImplementedError

    def register_query_handler(self, query: type[Q], handler: QueryHandlerType[Q, QRes]) -> None:
        raise NotImplementedError


class EventMediator(BaseMediator, Protocol):
    async def publish(self, events: Event | Sequence[Event], *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError

    def register_event_handler(self, event: type[E], handler: EventHandlerType[E]) -> None:
        raise NotImplementedError


class Mediator(CommandMediator, QueryMediator, EventMediator, BaseMediator, Protocol):
    pass
