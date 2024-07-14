from abc import abstractmethod
from typing import Any, Protocol, TypeVar


Q_contra = TypeVar("Q_contra", bound="Query", contravariant=True)
QRes_co = TypeVar("QRes_co", bound=Any, covariant=True)


class Query(Protocol): ...


class QueryHandler(Protocol[Q_contra, QRes_co]):
    @abstractmethod
    async def handle(self, query: Q_contra) -> QRes_co: ...
