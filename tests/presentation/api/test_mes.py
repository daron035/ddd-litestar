from faker import Faker

from src.application.messages.commands.create_chat import CreateChat
from src.infrastructure.mediator.mediator import MediatorImpl
from src.infrastructure.repositories.messages.base import BaseChatRepository
from src.domain.messages.entities.messages import Chat


async def test_create_chat_command_success(
    chat_repository: BaseChatRepository,
    mediator: MediatorImpl,
    faker: Faker,
):
    chat: Chat = await mediator.send(CreateChat(title=faker.text()))

    assert await chat_repository.check_chat_exists_by_title(title=chat.title.to_raw())
