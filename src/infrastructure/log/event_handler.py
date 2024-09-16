import logging

from src.domain.common.events import Event
from src.infrastructure.mediator.interface.handlers.event import EventHandler


logger = logging.getLogger(__name__)


class EventLogger(EventHandler[Event]):
    async def __call__(self, event: Event) -> None:
        logger.info("Event occurred", extra={"event_data": event})
