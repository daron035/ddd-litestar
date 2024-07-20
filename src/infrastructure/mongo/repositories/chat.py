from dataclasses import dataclass

from motor.core import AgnosticClient, AgnosticCollection

from src.application.messages.interfaces.percistence import ChatRepo
from src.domain.messages.entities.messages import Chat
from src.infrastructure.mongo.converters import convert_chat_entity_to_document


@dataclass
class MongoDBChatRepoImpl(ChatRepo):
    mongo_client: AgnosticClient
    mongo_db_name: str
    mongo_collection_name: str

    @property
    def _collection(self) -> AgnosticCollection:
        return self.mongo_client[self.mongo_db_name][self.mongo_collection_name]

    async def check_chat_exists_by_title(self, title: str) -> bool:
        return bool(await self._collection.find_one(filter={"title": title}))

    async def add_chat(self, chat: Chat) -> None:
        await self._collection.insert_one(convert_chat_entity_to_document(chat))
