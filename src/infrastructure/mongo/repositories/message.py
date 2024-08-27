from dataclasses import dataclass
from uuid import UUID

from pymongo import ASCENDING, DESCENDING

from src.application.common.pagination.dto import Pagination, PaginationResult, SortOrder
from src.application.messages import dto
from src.application.messages.interfaces.percistence import MessageReader, MessageRepo
from src.domain.common.constants import Empty
from src.domain.messages.entities.messages import Message
from src.infrastructure.mongo.converters import (
    convert_message_document_to_message_dto,
    convert_message_entity_to_document,
)
from src.infrastructure.mongo.repositories.base import MongoRepo


@dataclass
class MongoDBMessageReaderImpl(MongoRepo, MessageReader):
    async def get_messages_by_chat_id(self, chat_id: UUID, pagination: Pagination) -> dto.Messages:
        find = {"chat_id": str(chat_id)}

        sort_order = ASCENDING if pagination.order == SortOrder.ASC else DESCENDING

        cursor = self._collection.find(find).sort("created_at", sort_order)

        if pagination.offset is not Empty.UNSET:
            cursor = cursor.skip(pagination.offset)
        if pagination.limit is not Empty.UNSET:
            cursor = cursor.limit(pagination.limit)

        messages = [convert_message_document_to_message_dto(message_document) async for message_document in cursor]
        count = await self._collection.count_documents(filter=find)
        return dto.Messages(data=messages, pagination=PaginationResult.from_pagination(pagination, total=count))


@dataclass
class MongoDBMessageRepoImpl(MongoRepo, MessageRepo):
    async def add_message(self, message: Message) -> None:
        await self._collection.insert_one(
            document=convert_message_entity_to_document(message),
        )
