from src.application.common.exceptions import MappingError
from src.domain.common.events.event import Event
from src.domain.messages.events import ChatCreated, MessageCreated
from src.domain.user.events import UserCreated
from src.infrastructure.event_bus import events as integration_events


DomainEvents = Event | ChatCreated | MessageCreated | UserCreated


def convert_chat_created_to_integration(
    event: ChatCreated,
) -> integration_events.ChatCreated:
    return integration_events.ChatCreated(chat_id=event.chat_id, chat_title=event.chat_title)


def convert_message_created_to_integration(
    event: MessageCreated,
) -> integration_events.MessageCreated:
    return integration_events.MessageCreated(
        message_id=event.message_id,
        message_text=event.message_text,
        chat_id=event.chat_id,
    )


def convert_user_created_to_integration(
    event: UserCreated,
) -> integration_events.UserCreated:
    return integration_events.UserCreated(
        user_id=event.user_id,
        username=event.username,
        first_name=event.first_name,
        last_name=event.last_name,
    )


def convert_domain_event_to_integration(
    event: DomainEvents,
) -> integration_events.IntegrationEvent:
    match event:
        case ChatCreated():
            return convert_chat_created_to_integration(event)
        case MessageCreated():
            return convert_message_created_to_integration(event)
        case UserCreated():
            return convert_user_created_to_integration(event)
        case _:
            raise MappingError(f"Event {event} cannot be mapped to integration event")
