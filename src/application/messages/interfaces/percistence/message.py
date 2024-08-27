from abc import abstractmethod
from typing import Any, Protocol

from src.domain.messages.entities import Message


class MessageRepo(Protocol):
    @abstractmethod
    async def add_message(self, message: Message) -> Any:
        raise NotImplementedError
