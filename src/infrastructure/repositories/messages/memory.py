from dataclasses import dataclass, field

from src.domain.messages.entities.messages import Chat
from src.infrastructure.repositories.messages.base import BaseChatRepository


@dataclass
class MemoryChatRepository(BaseChatRepository):
    _saved_chats: list[Chat] = field(default_factory=list, kw_only=True)

    async def check_chat_exists_by_title(self, title: str) -> bool:
        try:
            return bool(next(chat for chat in self._saved_chats if chat.title.to_raw() == title))
        except StopIteration:
            return False

    async def add_chat(self, chat: Chat) -> None:
        self._saved_chats.append(chat)
