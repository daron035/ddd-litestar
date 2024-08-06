from dataclasses import dataclass

from motor.core import AgnosticClient, AgnosticCollection


@dataclass
class MongoRepo:
    mongo_client: AgnosticClient
    mongo_db_name: str
    mongo_collection_name: str

    @property
    def _collection(self) -> AgnosticCollection:
        return self.mongo_client[self.mongo_db_name][self.mongo_collection_name]
