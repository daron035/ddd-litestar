from dataclasses import dataclass
from uuid import UUID

from .base import IntegrationEvent, integration_event


@dataclass(frozen=True)
@integration_event(topic="User", key=b"UserCreated")
class UserCreated(IntegrationEvent):
    user_id: UUID
    username: str
    first_name: str
    last_name: str | None
