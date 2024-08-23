from typing import Any
from uuid import UUID

from litestar import (
    MediaType,
    get,
    post,
)
from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.openapi import ResponseSpec
from litestar.status_codes import HTTP_400_BAD_REQUEST
from punq import Container

from src.application.common.exceptions import ApplicationError
from src.application.messages.commands.create_chat import CreateChat
from src.application.messages.commands.create_message import CreateMessage
from src.infrastructure.containers import init_container
from src.infrastructure.mediator.mediator import MediatorImpl


@post(
    path="/",
    description="Endpoint creates a new chat room, if a chat room with that name exists, a 400 error is returned",
    dependencies={"container": Provide(init_container, sync_to_thread=False)},
    responses={
        201: ResponseSpec(None, description="Chat successfully created"),
        400: ResponseSpec(None, description="Error occured"),
    },
)
async def create_chat(data: CreateChat, container: Container) -> Any:
    mediator: MediatorImpl = container.resolve(MediatorImpl)

    try:
        chat = await mediator.send(data)
    except ApplicationError as exception:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"{exception.title}") from exception

    return chat


@post(
    path="/{chat_id:uuid}/messages",
    description="Add new message to chat with Id",
    dependencies={"container": Provide(init_container, sync_to_thread=False)},
    responses={
        201: ResponseSpec(None, description="Chat successfully created"),
        400: ResponseSpec(None, description="Error occured"),
    },
)
async def create_message(data: str, chat_id: UUID, container: Container) -> Any:
    mediator: MediatorImpl = container.resolve(MediatorImpl)

    try:
        message = await mediator.send(CreateMessage(text=data, chat_id=chat_id))
    except ApplicationError as exception:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"{exception.title}") from exception

    return message


@get("/books/{book_id:int}")
async def get_book(book_id: int) -> dict[str, int]:
    return {"book_id": book_id}


@get(path="/healthcheck", media_type=MediaType.TEXT, sync_to_thread=False)
def health_check() -> str:
    return "healthy"
