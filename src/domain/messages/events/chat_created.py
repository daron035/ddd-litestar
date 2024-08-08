from dataclasses import dataclass
from uuid import UUID

from src.domain.common.events.event import Event


@dataclass(frozen=True)
class ChatCreated(Event):
    chat_id: UUID
    chat_title: str
