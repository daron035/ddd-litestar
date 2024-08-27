from dataclasses import dataclass
from uuid import UUID

from src.application.common.pagination.dto import Pagination
from src.application.messages import dto
from src.application.messages.interfaces.percistence.reader import MessageReader
from src.infrastructure.mediator.interface.entities.query import Query
from src.infrastructure.mediator.interface.handlers.query import QueryHandler


@dataclass(frozen=True)
class GetMessagesByChatId(Query[dto.Messages]):
    chat_id: UUID
    pagination: Pagination


@dataclass(frozen=True)
class GetMessagesByChatIdHandler(QueryHandler[GetMessagesByChatId, dto.Messages]):
    messages_repository: MessageReader

    async def __call__(self, query: GetMessagesByChatId) -> dto.Messages:
        messages = await self.messages_repository.get_messages_by_chat_id(
            chat_id=query.chat_id,
            pagination=query.pagination,
        )

        return messages
