from typing import Any
from uuid import UUID

from injector import Injector
from litestar import (
    MediaType,
    get,
    post,
    status_codes,
)
from litestar.di import Provide

from src.application.messages.commands.create_chat import CreateChat
from src.application.messages.commands.create_message import CreateMessage
from src.infrastructure.ioc import init_container
from src.infrastructure.mediator.mediator import MediatorImpl


@post(
    path="/",
    description="Endpoint creates a new chat room, if a chat room with that name exists, a 400 error is returned",
    dependencies={"container": Provide(init_container, sync_to_thread=False)},
    status_code=status_codes.HTTP_201_CREATED,
)
async def index(data: CreateChat, container: Injector) -> Any:
    mediator = container.get(MediatorImpl)

    chat = await mediator.send(data)
    return chat


@post(
    path="/{chat_id:uuid}/messages",
    description="Add new message to chat with Id",
    dependencies={"container": Provide(init_container, sync_to_thread=False)},
    status_code=status_codes.HTTP_201_CREATED,
)
async def create_message(data: str, chat_id: UUID, container: Injector) -> Any:
    mediator = container.get(MediatorImpl)

    message = await mediator.send(CreateMessage(text=data, chat_id=chat_id))
    return message


@get("/books/{book_id:int}")
async def get_book(book_id: int) -> dict[str, int]:
    return {"book_id": book_id}


@get(path="/healthcheck", media_type=MediaType.TEXT, sync_to_thread=False)
def health_check() -> str:
    return "healthy"
