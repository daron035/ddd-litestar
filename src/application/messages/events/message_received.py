from dataclasses import dataclass

from src.application.messages.websockets.managers import WebSocketConnectionManager
from src.infrastructure.event_bus.events.message_created import MessageCreated
from src.infrastructure.mediator.interface.handlers.event import EventHandler


@dataclass(frozen=True)
class MessageReceived(MessageCreated):
    pass


@dataclass(frozen=True)
class MessageReceivedHandler(EventHandler[MessageReceived]):
    _ws_manager: WebSocketConnectionManager

    async def __call__(self, event: MessageReceived, *args, **kwargs) -> None:
        print()
        print()
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("MessageReceivedHandler")
        print(event)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print()
        print()
