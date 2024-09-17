from dataclasses import dataclass
from uuid import UUID

from src.application.messages.interfaces.percistence.chat import ChatRepo
from src.application.messages.interfaces.percistence.message import MessageRepo
from src.domain.common.value_objects.id import Id
from src.domain.messages.entities.messages import Chat, Message
from src.domain.messages.value_objects import Text
from src.infrastructure.mediator.interface.entities.command import Command
from src.infrastructure.mediator.interface.handlers.command import CommandHandler
from src.infrastructure.mediator.interface.mediator import EventMediator


@dataclass(frozen=True)
class CreateMessage(Command[Message]):
    text: str
    chat_id: UUID


@dataclass(frozen=True)
class CreateMessageHandler(CommandHandler[CreateMessage, Message]):
    chat_repository: ChatRepo
    message_repository: MessageRepo
    mediator: EventMediator

    async def __call__(self, command: CreateMessage) -> Message:
        chat: Chat = await self.chat_repository.get_chat_by_id(chat_id=command.chat_id)

        message = Message(text=Text(value=command.text), chat_id=Id(value=command.chat_id))
        chat.add_message(message)
        await self.message_repository.add_message(message=message)
        await self.mediator.publish(chat.pull_events())

        return message
