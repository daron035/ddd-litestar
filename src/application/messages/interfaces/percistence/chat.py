from abc import abstractmethod
from typing import Protocol

from src.domain.messages import entities


class ChatRepo(Protocol):
    @abstractmethod
    async def check_chat_exists_by_title(self, title: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def add_chat(self, chat: entities.Chat) -> None:
        raise NotImplementedError
