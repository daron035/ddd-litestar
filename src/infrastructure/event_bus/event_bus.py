from dataclasses import dataclass

from src.infrastructure.message_broker.interface import MessageBroker


@dataclass
class EventBusImpl:
    _message_broker: MessageBroker

    async def publish_message(self, topic: str, key: bytes, value: bytes) -> None:
        await self._message_broker.publish_message(topic=topic, key=key, value=value)
