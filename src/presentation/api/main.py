import logging
from uuid import UUID

from injector import Injector
from litestar import (
    Litestar,
    MediaType,
    get,
    post,
)
from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.status_codes import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from pydantic import BaseModel
from src.application.common.mediator.base import Mediator
from src.application.messages.commands.create_chat import CreateChat
from src.domain.common.exceptions.base import AppError
from src.domain.messages.entities.messages import Chat
from src.infrastructure.ioc import init_container


class CreateChatRequestSchema(BaseModel):
    title: str


class CreateChatResponseSchema(BaseModel):
    id: UUID
    title: str

    @classmethod
    def from_entity(cls, chat: Chat) -> "CreateChatResponseSchema":
        return cls(
            id=chat.id,
            title=chat.title.to_raw(),
        )


class ErrorSchema(BaseModel):
    error: str


@post(
    path="/",
    description="Endpoint creates a new chat room, if a chat room with that name exists, a 400 error is returned",
    dependencies={"container": Provide(init_container, sync_to_thread=False)},
    status_code=HTTP_201_CREATED,
)
async def index(data: CreateChatRequestSchema, container: Injector) -> CreateChatResponseSchema:
    mediator = container.get(Mediator)

    try:
        chat, *_ = await mediator.send(CreateChat(title=data.title))
    except AppError as exception:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, extra={"error": exception.title}) from exception

    return CreateChatResponseSchema.from_entity(chat)


@get("/books/{book_id:int}")
async def get_book(book_id: int) -> dict[str, int]:
    return {"book_id": book_id}


@get(path="/health-check", media_type=MediaType.TEXT, sync_to_thread=False)
def health_check() -> str:
    return "healthy"


def create_app() -> Litestar:
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s  %(process)-7s %(module)-20s %(message)s",
    )
    app = Litestar(route_handlers=[index, get_book, health_check], debug=True)
    return app
