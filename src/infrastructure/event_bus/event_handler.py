from dataclasses import dataclass

from src.domain.common.events.event import Event
from src.infrastructure.mediator.interface.handlers.event import EventHandler
from src.infrastructure.message_broker.interface import MessageBroker


@dataclass
class EventHandlerPublisher(EventHandler[Event]):
    message_broker: MessageBroker

    async def __call__(self, event: Event) -> None:
        await self.message_broker.publish_message(
            topic="test-topic",
            key=b"event_key",
            value=b"event_value",
        )
