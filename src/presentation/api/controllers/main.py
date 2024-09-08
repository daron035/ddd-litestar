from typing import Annotated, Any
from uuid import UUID

from litestar import MediaType, get, post
from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.openapi import ResponseSpec
from litestar.params import Parameter
from litestar.status_codes import HTTP_400_BAD_REQUEST
from punq import Container

from src.application.common.exceptions import ApplicationError
from src.application.common.pagination.dto import Pagination, SortOrder
from src.application.messages.commands.create_chat import CreateChat
from src.application.messages.commands.create_message import CreateMessage
from src.application.messages.queries.get_messages_by_chat import GetMessagesByChatId
from src.application.user.commands.create_user import CreateUser
from src.infrastructure.containers import init_container
from src.infrastructure.mediator.mediator import MediatorImpl
from src.infrastructure.postgres.services.healthcheck import PgHealthCheck


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


@get(
    path="/{chat_id:uuid}/messages",
    description="Grab all messages from certain chat room",
    dependencies={
        "container": Provide(init_container, sync_to_thread=False),
    },
    responses={
        200: ResponseSpec(None, description="Messages received"),
        400: ResponseSpec(None, description="Error occured"),
    },
)
async def get_chat_messages(
    chat_id: UUID,
    offset: Annotated[int, Parameter(ge=0, default=0)],
    limit: Annotated[int, Parameter(gt=0, default=10)],
    order: Annotated[SortOrder, Parameter(default=SortOrder.ASC)],
    container: Container,
) -> Any:
    mediator: MediatorImpl = container.resolve(MediatorImpl)

    try:
        messages = await mediator.query(
            GetMessagesByChatId(
                chat_id=chat_id,
                pagination=Pagination(
                    offset=offset,
                    limit=limit,
                    order=order,
                ),
            ),
        )
    except ApplicationError as exception:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"{exception.title}") from exception

    return messages


@get("/books/{book_id:int}")
async def get_book(book_id: int) -> dict[str, int]:
    return {"book_id": book_id}


@get(path="/healthcheck", media_type=MediaType.TEXT, sync_to_thread=False)
def health_check() -> str:
    return "healthy"


@get(
    path="/test-db-connection",
    description="Example of an endpoint using a SQLAlchemy session",
    dependencies={
        "container": Provide(init_container, sync_to_thread=False),
    },
)
async def test_postgres_db(
    container: Container,
) -> Any:
    psql: PgHealthCheck = container.resolve(PgHealthCheck)
    response = await psql.check()
    return response


@post(
    path="/user",
    description="Create new user",
    dependencies={"container": Provide(init_container, sync_to_thread=False)},
    responses={
        201: ResponseSpec(None, description="Chat successfully created"),
        400: ResponseSpec(None, description="Error occured"),
    },
)
async def create_user(data: CreateUser, container: Container) -> Any:
    mediator: MediatorImpl = container.resolve(MediatorImpl)

    try:
        chat = await mediator.send(data)
    except ApplicationError as exception:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"{exception.title}") from exception

    return chat
