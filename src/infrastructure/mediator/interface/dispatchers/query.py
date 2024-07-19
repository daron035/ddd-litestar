from typing import Any, Protocol, TypeVar

from src.infrastructure.mediator.interface.dispatchers.request import Dispatcher
from src.infrastructure.mediator.interface.entities.query import Query
from src.infrastructure.mediator.interface.handlers.query import QueryHandlerType


Q = TypeVar("Q", bound=Query[Any])
QRes = TypeVar("QRes")


class QueryDispatcher(Dispatcher, Protocol):
    def register_handler(self, query: type[Q], handler: QueryHandlerType[Q, QRes]) -> None:
        raise NotImplementedError

    async def query(self, query: Query[QRes], *args: Any, **kwargs: Any) -> QRes:
        raise NotImplementedError
