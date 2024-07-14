from faker import Faker

from src.application.common.mediator.base import Mediator
from src.application.messages.commands.create_chat import CreateChat
from src.infrastructure.repositories.messages.base import BaseChatRepository

# from src.domain.values.messages import Title
# # from infra.repositories.messages.base import BaseChatsRepository
# from logic.commands.messages import CreateChatCommand
# from logic.exceptions.messages import ChatWithThatTitleAlreadyExistsException
# # from logic.mediator.base import Mediator


# @pytest.mark.asyncio
async def test_create_chat_command_success(
    chat_repository: BaseChatRepository,
    mediator: Mediator,
    faker: Faker,
):
    # TODO: Закинуть фейкер для генерации рандомных текстов
    # chat: Chat
    chat, *_ = await mediator.send(CreateChat(title=faker.text()))

    assert await chat_repository.check_chat_exists_by_title(title=chat.title.to_raw())


# @pytest.mark.asyncio
# async def test_create_chat_command_title_already_exists(
#     chat_repository: BaseChatsRepository,
#     mediator: Mediator,
#     faker: Faker,
# ):
#     # TODO: Закинуть фейкер для генерации рандомных текстов
#     title_text = faker.text()
#     chat = Chat(title=Title(title_text))
#     await chat_repository.add_chat(chat)

#     assert chat in chat_repository._saved_chats

#     with pytest.raises(ChatWithThatTitleAlreadyExistsException):
#         await mediator.handle_command(CreateChatCommand(title=title_text))

#     assert len(chat_repository._saved_chats) == 1
