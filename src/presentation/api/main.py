from typing import Any

from injector import Injector
from litestar import (
    Litestar,
    MediaType,
    get,
    post,
    status_codes,
)
from litestar.di import Provide

from src.application.messages.commands.create_chat import CreateChat
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


@get("/books/{book_id:int}")
async def get_book(book_id: int) -> dict[str, int]:
    return {"book_id": book_id}


@get(path="/health-check", media_type=MediaType.TEXT, sync_to_thread=False)
def health_check() -> str:
    return "healthy"


def create_app() -> Litestar:
    app = Litestar(route_handlers=[index, get_book, health_check], debug=True)
    return app
