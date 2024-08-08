from abc import abstractmethod
from typing import Protocol


class MessageBroker(Protocol):
    @abstractmethod
    async def publish_message(
        self,
        topic: str,
        key: bytes,
        value: bytes,
        partition: int | None,
        headers: list[tuple[str, bytes]] | None,
    ) -> None:
        raise NotImplementedError
