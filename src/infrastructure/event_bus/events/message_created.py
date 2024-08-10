from dataclasses import dataclass
from uuid import UUID

from .base import IntegrationEvent, integration_event


@dataclass(frozen=True)
@integration_event(topic="Message", key=b"MessageCreated")
class MessageCreated(IntegrationEvent):
    message_id: UUID
    message_text: str
    chat_id: UUID
