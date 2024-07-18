from dataclasses import dataclass

from src.application.messages.exceptions import ChatWithThatTitleAlreadyExistsError
from src.domain.common.entities.entity import Entity
from src.domain.messages.entities.messages import Chat
from src.domain.messages.value_objects import Title
from src.infrastructure.mediator.interface.entities.command import Command
from src.infrastructure.mediator.interface.handlers.command import CommandHandler
from src.infrastructure.repositories.messages.base import BaseChatRepository


@dataclass(frozen=True)
class CreateChat(Command[Chat]):
    title: str


@dataclass(frozen=True)
class CreateChatHandler(CommandHandler[CreateChat, Entity]):
    chat_repository: BaseChatRepository

    async def __call__(self, command: CreateChat) -> Entity:
        if await self.chat_repository.check_chat_exists_by_title(command.title):
            raise ChatWithThatTitleAlreadyExistsError(command.title)

        title = Title(value=command.title)

        new_chat = Chat.create(title=title)
        await self.chat_repository.add_chat(new_chat)

        return new_chat
