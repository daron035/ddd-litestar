from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

import orjson

from src.infrastructure.event_bus.events.base import IntegrationEvent
from src.infrastructure.message_broker.interface import MessageBroker
from src.infrastructure.message_broker.message import Message


@dataclass
class EventBusImpl:
    _message_broker: MessageBroker

    async def publish_message(self, event: IntegrationEvent) -> None:
        message = self.build_message(event)
        await self._message_broker.publish_message(
            topic=message.topic,
            key=message.key,
            value=message.value,
            partition=None,
            headers=message.headers,
        )

    @staticmethod
    def build_message(event: IntegrationEvent) -> Message:
        return Message(
            topic=event.topic,
            key=event.key,
            value=serialize_event_data(event),
            headers=[("header-key", b"header-value")],
        )


def serialize_event_data(event: Any) -> bytes:
    event_dict = asdict(event)
    serialized_event = orjson.dumps({k: serialize_event(v) for k, v in event_dict.items()})
    return serialized_event


def serialize_event(obj: Any) -> Any:  # noqa: PLR0911
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: serialize_event(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [serialize_event(item) for item in obj]
    if isinstance(obj, tuple):
        return tuple(serialize_event(item) for item in obj)
    if isinstance(obj, set):
        return set(serialize_event(item) for item in obj)
    return obj
