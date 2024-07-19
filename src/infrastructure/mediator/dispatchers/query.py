from typing import Any, TypeVar

from src.infrastructure.mediator.dispatchers.request import DispatcherImpl
from src.infrastructure.mediator.interface.dispatchers.query import QueryDispatcher
from src.infrastructure.mediator.interface.entities.query import Query
from src.infrastructure.mediator.interface.exceptions import HandlerNotFoundError, QueryHandlerNotFoundError
from src.infrastructure.mediator.interface.handlers.request import HandlerType


QRes = TypeVar("QRes")
Q = TypeVar("Q", bound=Query[Any])


class QueryDispatcherImpl(DispatcherImpl, QueryDispatcher):
    def register_handler(self, query: type[Q], handler: HandlerType[Q, QRes]) -> None:
        super()._register_handler(query, handler)

    async def query(self, query: Query[QRes], *args: Any, **kwargs: Any) -> QRes:
        try:
            return await self._handle(query, *args, **kwargs)
        except HandlerNotFoundError as err:
            raise QueryHandlerNotFoundError(
                f"Query handler for {type(query).__name__} query is not registered",
                query,
            ) from err
