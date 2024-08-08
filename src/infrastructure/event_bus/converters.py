from src.application.common.exceptions import MappingError
from src.domain.messages.events import ChatCreated
from src.infrastructure.event_bus import events as integration_events


DomainEvents = ChatCreated


def convert_chat_created_to_integration(
    event: ChatCreated,
) -> integration_events.ChatCreated:
    return integration_events.ChatCreated(chat_id=event.chat_id, chat_title=event.chat_title)


def convert_domain_event_to_integration(
    event: DomainEvents,
) -> integration_events.IntegrationEvent:
    match event:
        case ChatCreated():
            return convert_chat_created_to_integration(event)
        case _:
            raise MappingError(f"Event {event} cannot be mapped to integration event")
