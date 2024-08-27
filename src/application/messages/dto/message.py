from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.application.common.dto import DTO


@dataclass(frozen=True)
class Message(DTO):
    id: UUID
    text: str
    chat_id: UUID
    created_at: datetime
