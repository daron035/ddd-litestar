from abc import abstractmethod
from typing import Any, Protocol

from src.domain.messages.entities import Message


class MessageRepo(Protocol):
    @abstractmethod
    async def add_message(self, message: Message) -> Any: ...

    # @abstractmethod
    # async def get_messages(
    #     # self, chat_oid: str, filters: GetMessagesFilters
    #     self,
    #     chat_oid: str,
    # ) -> tuple[Iterable[Message], int]: ...
