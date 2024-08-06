from abc import abstractmethod
from typing import Protocol


class MessageBroker(Protocol):
    @abstractmethod
    async def publish_message(self, topic: str, key: bytes, value: bytes) -> None:
        raise NotImplementedError
