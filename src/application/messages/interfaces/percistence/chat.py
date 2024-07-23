from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.domain.messages import entities
from src.domain.messages.entities.messages import Chat


class ChatRepo(Protocol):
    @abstractmethod
    async def add_chat(self, chat: entities.Chat) -> None:
        raise NotImplementedError

    @abstractmethod
    async def check_chat_exists_by_title(self, title: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_chat_by_id(self, chat_id: UUID) -> Chat | None:
        raise NotImplementedError
