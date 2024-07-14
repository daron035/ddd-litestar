from dataclasses import dataclass

from src.application.common.command import Command, CommandHandler
from src.application.messages.exceptions import ChatWithThatTitleAlreadyExistsError
from src.domain.messages.entities.messages import Chat
from src.domain.messages.value_objects import Title
from src.infrastructure.repositories.messages.base import BaseChatRepository


@dataclass(frozen=True)
class CreateChat(Command):
    title: str


@dataclass(frozen=True)
# @inject
class CreateChatHandler(CommandHandler[CreateChat, Chat]):
    chat_repository: BaseChatRepository

    async def handle(self, command: CreateChat) -> Chat:
        if await self.chat_repository.check_chat_exists_by_title(command.title):
            raise ChatWithThatTitleAlreadyExistsError(command.title)

        title = Title(value=command.title)

        new_chat = Chat.create(title=title)
        await self.chat_repository.add_chat(new_chat)

        return new_chat
