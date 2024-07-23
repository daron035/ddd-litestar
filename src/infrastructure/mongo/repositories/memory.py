from dataclasses import dataclass, field
from uuid import UUID

from src.application.messages.interfaces.percistence import ChatRepo
from src.domain.messages.entities.messages import Chat


@dataclass
class MemoryChatRepoImpl(ChatRepo):
    _saved_chats: list[Chat] = field(default_factory=list, kw_only=True)

    async def check_chat_exists_by_title(self, title: str) -> bool:
        try:
            return bool(next(chat for chat in self._saved_chats if chat.title.to_raw() == title))
        except StopIteration:
            return False

    async def add_chat(self, chat: Chat) -> None:
        self._saved_chats.append(chat)

    async def get_chat_by_id(self, chat_id: UUID) -> Chat | None:
        pass
