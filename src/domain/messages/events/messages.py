from dataclasses import dataclass
from uuid import UUID

from src.domain.common.events.event import Event


@dataclass(frozen=True)
class NewMessageReceivedEvent(Event):
    message_id: UUID
    message_text: str
    chat_id: UUID


@dataclass(frozen=True)
class ListenerAddedEvent(Event):
    listener_id: UUID


@dataclass(frozen=True)
class ChatDeletedEvent(Event):
    chat_id: UUID
