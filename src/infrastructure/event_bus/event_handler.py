from dataclasses import dataclass

from src.domain.common.events.event import Event
from src.infrastructure.event_bus.event_bus import EventBusImpl
from src.infrastructure.mediator.interface.handlers.event import EventHandler


@dataclass
class EventHandlerPublisher(EventHandler[Event]):
    _event_bus: EventBusImpl

    async def __call__(self, event: Event) -> None:
        await self._event_bus.publish_message(
            topic="test-topic",
            key=b"event_key",
            value=b"event_value",
        )
