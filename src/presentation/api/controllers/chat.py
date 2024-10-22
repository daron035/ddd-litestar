import logging

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from punq import Container

from src.application.common.pagination.dto import Pagination, SortOrder
from src.application.messages.commands.create_chat import CreateChat
from src.application.messages.commands.create_message import CreateMessage
from src.application.messages.queries.get_messages_by_chat import GetMessagesByChatId
from src.domain.messages.value_objects.text import EmptyTextError, TooLongTextError
from src.infrastructure.containers import init_container
from src.infrastructure.mediator.mediator import MediatorImpl
from src.presentation.api.controllers.responses.base import ErrorResponse


logger = logging.getLogger(__name__)


chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@chat_router.post(
    path="/",
    description="Endpoint creates a new chat room, if a chat room with that name exists, a 400 error is returned",
)
async def create_chat(
    data: CreateChat,
    container: Container = Depends(init_container),
) -> dict:
    mediator: MediatorImpl = container.resolve(MediatorImpl)
    chat = await mediator.send(data)

    return {"chat_id": chat.id.to_raw()}


from src.application.messages import dto


@chat_router.post(
    path="/{chat_id}/messages",
    description="Add new message to chat with Id",
    responses={
        status.HTTP_201_CREATED: {"model": dto.Message},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[EmptyTextError | TooLongTextError],
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_message(data: str, chat_id: UUID, container: Container = Depends(init_container)) -> dto.Message:
    mediator: MediatorImpl = container.resolve(MediatorImpl)
    message = await mediator.send(CreateMessage(text=data, chat_id=chat_id))
    message_dto = dto.Message.from_entity(message)

    return message_dto


@chat_router.get(
    path="/{chat_id}/messages",
)
async def get_chat_messages(
    chat_id: UUID,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=1000)] = 1000,
    order: SortOrder = SortOrder.ASC,
    container: Container = Depends(init_container),
) -> dto.Messages:
    mediator: MediatorImpl = container.resolve(MediatorImpl)

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

    return messages
