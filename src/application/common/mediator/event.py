from abc import ABC, abstractmethod
from collections.abc import Iterable, Sequence
from typing import Generic

from src.application.common.event import E_contra, ERes_co, EventHandler
from src.domain.common.events.event import Event


class EventMediator(ABC, Generic[E_contra, ERes_co]):
    @abstractmethod
    def register_event(self, event: E_contra, event_handlers: Iterable[EventHandler[E_contra, ERes_co]]) -> None: ...

    @abstractmethod
    async def publish(self, events: Sequence[Event]) -> None: ...
