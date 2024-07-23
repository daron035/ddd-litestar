from abc import abstractmethod
from collections.abc import Iterable
from typing import Protocol

from src.domain.messages.entities import Message


class MessageRepo(Protocol):
    @abstractmethod
    async def add_message(self, message: Message) -> None: ...

    @abstractmethod
    async def get_messages(
        # self, chat_oid: str, filters: GetMessagesFilters
        self,
        chat_oid: str,
    ) -> tuple[Iterable[Message], int]: ...
