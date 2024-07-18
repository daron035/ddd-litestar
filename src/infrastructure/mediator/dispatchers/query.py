from typing import Any, TypeVar

from src.infrastructure.mediator.dispatchers.request import DispatcherImpl
from src.infrastructure.mediator.interface.dispatchers.query import QueryDispatcher
from src.infrastructure.mediator.interface.entities.query import Query
from src.infrastructure.mediator.interface.exceptions import HandlerNotFound, QueryHandlerNotFound
from src.infrastructure.mediator.interface.handlers.request import HandlerType

# from src.application.common.mediator.dispatchers import DispatcherImpl
# from src.application.common.mediator.interface.dispatchers import QueryDispatcher
# from src.application.common.mediator.interface.entities import Query
# from src.application.common.mediator.interface.exceptions import HandlerNotFound, QueryHandlerNotFound
# from src.application.common.mediator.interface.handlers import HandlerType


QRes = TypeVar("QRes")
Q = TypeVar("Q", bound=Query[Any])


class QueryDispatcherImpl(DispatcherImpl, QueryDispatcher):
    def register_handler(self, query: type[Q], handler: HandlerType[Q, QRes]) -> None:
        super()._register_handler(query, handler)

    async def query(self, query: Query[QRes], *args: Any, **kwargs: Any) -> QRes:
        try:
            return await self._handle(query, *args, **kwargs)
        except HandlerNotFound as err:
            raise QueryHandlerNotFound(
                f"Query handler for {type(query).__name__} query is not registered", query,
            ) from err
