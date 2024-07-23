from dataclasses import dataclass
from uuid import UUID

from src.application.messages.interfaces.percistence import ChatRepo
from src.domain.messages.entities.messages import Chat
from src.infrastructure.mongo.converters import convert_chat_document_to_entity, convert_chat_entity_to_document
from src.infrastructure.mongo.repositories.base import MongoRepo


@dataclass
class MongoDBChatRepoImpl(MongoRepo, ChatRepo):
    async def add_chat(self, chat: Chat) -> None:
        await self._collection.insert_one(convert_chat_entity_to_document(chat))

    async def check_chat_exists_by_title(self, title: str) -> bool:
        return bool(await self._collection.find_one(filter={"title": title}))

    async def get_chat_by_id(self, chat_id: UUID) -> Chat | None:
        chat_document = await self._collection.find_one(filter={"id": str(chat_id)})

        if not chat_document:
            return None

        return convert_chat_document_to_entity(chat_document)
