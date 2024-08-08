from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar, TypeVar
from uuid import UUID

from uuid6 import uuid7


@dataclass(frozen=True, kw_only=True)
class IntegrationEvent:
    event_id: UUID = field(default_factory=uuid7)
    event_timestamp: datetime = field(default_factory=datetime.now)
    topic: ClassVar[str]
    key: ClassVar[bytes]


EventType = TypeVar("EventType", bound=type[IntegrationEvent])


def integration_event(
    topic: str,
    key: bytes,
) -> Callable[[EventType], EventType]:
    def _integration_event(cls: EventType) -> EventType:
        cls.topic = topic
        cls.key = key
        return cls

    return _integration_event
