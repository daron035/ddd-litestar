from abc import abstractmethod
from typing import Protocol

from src.domain.common.events.event import Event


class OutboxRepo(Protocol):
    @abstractmethod
    async def save(self, event: Event | list[Event]) -> None:
        raise NotImplementedError
