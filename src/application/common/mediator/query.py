from abc import ABC, abstractmethod
from typing import Generic

from src.application.common.query import Q_contra, QRes_co, Query, QueryHandler


class QueryMediator(ABC, Generic[Q_contra, QRes_co]):
    @abstractmethod
    def register_query(self, query: Q_contra, query_handler: QueryHandler[Q_contra, QRes_co]) -> None: ...

    @abstractmethod
    async def query(self, query: Query) -> QRes_co: ...
