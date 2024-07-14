from abc import abstractmethod
from typing import Any, Protocol, TypeVar

from src.domain.common.events import Event


E_contra = TypeVar("E_contra", bound=Event, contravariant=True)
ERes_co = TypeVar("ERes_co", bound=Any, covariant=True)


class EventHandler(Protocol[E_contra, ERes_co]):
    @abstractmethod
    def handle(self, event: E_contra) -> ERes_co: ...
