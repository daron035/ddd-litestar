from dataclasses import dataclass

from src.application.common.exceptions import MappingError
from src.domain.common.events.event import Event
from src.infrastructure.event_bus.converters import convert_domain_event_to_integration
from src.infrastructure.event_bus.event_bus import EventBusImpl
from src.infrastructure.mediator.interface.handlers.event import EventHandler


@dataclass
class EventHandlerPublisher(EventHandler[Event]):
    _event_bus: EventBusImpl

    async def __call__(self, event: Event) -> None:
        try:
            integration_event = convert_domain_event_to_integration(event)
        except MappingError:
            return

        await self._event_bus.publish_message(integration_event)
