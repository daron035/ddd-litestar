from dataclasses import dataclass
from uuid import UUID

from src.domain.common.events.event import Event


@dataclass(frozen=True)
class MessageCreated(Event):
    message_id: UUID
    message_text: str
    chat_id: UUID
