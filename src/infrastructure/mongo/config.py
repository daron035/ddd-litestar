from dataclasses import dataclass


@dataclass
class MongoConfig:
    mongodb_connection_uri: str = "mongodb://mongodb:27017"
    mongodb_chat_database: str = "chat"
    mongodb_chat_collection: str = "chat"
