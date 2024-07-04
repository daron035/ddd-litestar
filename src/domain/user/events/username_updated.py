from dataclasses import dataclass
from uuid import UUID

from src.domain.common.events.event import Event


@dataclass(frozen=True)
class UsernameUpdated(Event):
    user_id: UUID
    username: str
