from dataclasses import dataclass

import orjson

from src.application.messages.websockets.managers import WebSocketConnectionManager
from src.infrastructure.mediator.interface.entities.event import Event
from src.infrastructure.mediator.interface.handlers.event import EventHandler


@dataclass(frozen=True)
class MessageReceived(Event):
    message_id: str
    message_text: str
    chat_id: str


@dataclass(frozen=True)
class MessageReceivedHandler(EventHandler[MessageReceived]):
    _ws_manager: WebSocketConnectionManager

    async def __call__(self, event: MessageReceived) -> None:
        await self._ws_manager.send_all(key=event.chat_id, bytes_=convert_event_to_broker_message(event))


def convert_event_to_broker_message(event: Event) -> bytes:
    return orjson.dumps(event)
