from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

from src.domain.messages.entities.messages import Chat


@dataclass
# class BaseChatRepository(ABC):
class BaseChatRepository(Protocol):
    @abstractmethod
    async def check_chat_exists_by_title(self, title: str) -> bool: ...

    @abstractmethod
    async def add_chat(self, chat: Chat) -> None: ...
