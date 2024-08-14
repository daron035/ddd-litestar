from abc import abstractmethod
from collections.abc import AsyncIterator
from typing import Protocol


class MessageBroker(Protocol):
    @abstractmethod
    async def publish_message(  # noqa: PLR0913
        self,
        topic: str,
        key: bytes,
        value: bytes,
        partition: int | None,
        headers: list[tuple[str, bytes]] | None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def start_consuming(self, topic: str) -> AsyncIterator[dict]:
        raise NotImplementedError
