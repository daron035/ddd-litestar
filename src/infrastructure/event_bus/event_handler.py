from dataclasses import dataclass

from src.domain.common.events.event import Event
from src.infrastructure.mediator.interface.handlers.event import EventHandler
from src.kafka_test_producer import send_one


@dataclass
class EventHandlerPublisher(EventHandler[Event]):

    async def __call__(self, event: Event) -> None:
        await send_one()
