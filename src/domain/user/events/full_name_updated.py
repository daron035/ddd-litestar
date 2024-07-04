from dataclasses import dataclass
from uuid import UUID

from src.domain.common.events.event import Event


@dataclass(frozen=True)
class FullNameUpdated(Event):
    user_id: UUID
    first_name: str
    last_name: str
    middle_name: str | None
