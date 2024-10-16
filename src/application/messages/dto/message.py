from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.application.common.dto import DTO
from src.domain.messages.entities.messages import Message as MessageEntity


@dataclass(frozen=True)
class Message(DTO):
    id: UUID
    text: str
    chat_id: UUID
    created_at: datetime

    @staticmethod
    def from_entity(entity: MessageEntity) -> "Message":
        return Message(
            id=entity.id.to_raw(),
            text=entity.text.to_raw(),
            chat_id=entity.chat_id.to_raw(),
            created_at=entity.created_at,
        )
