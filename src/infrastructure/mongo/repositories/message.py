from collections.abc import Iterable
from dataclasses import dataclass

from src.application.messages.interfaces.percistence.message import MessageRepo
from src.domain.messages.entities.messages import Message
from src.infrastructure.mongo.converters import convert_message_entity_to_document
from src.infrastructure.mongo.repositories.base import MongoRepo


@dataclass
class MongoDBMessageRepoImpl(MongoRepo, MessageRepo):
    async def add_message(self, message: Message) -> None:
        await self._collection.insert_one(
            document=convert_message_entity_to_document(message),
        )

    async def get_messages(self, chat_oid: str) -> tuple[Iterable[Message], int]:
        return None  # type: ignore
