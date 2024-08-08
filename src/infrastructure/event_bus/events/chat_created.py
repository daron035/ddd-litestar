from dataclasses import dataclass
from uuid import UUID

from .base import IntegrationEvent, integration_event


@dataclass(frozen=True)
@integration_event(topic="Chat", key=b"ChatCreated")
class ChatCreated(IntegrationEvent):
    chat_id: UUID
    chat_title: str
