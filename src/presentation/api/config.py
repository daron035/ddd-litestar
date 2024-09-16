from dataclasses import dataclass, field

from src.infrastructure.log import LoggingConfig
from src.infrastructure.message_broker.config import EventBusConfig
from src.infrastructure.mongo.config import MongoConfig
from src.infrastructure.postgres.config import PostgresConfig


@dataclass
class APIConfig:
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = __debug__


@dataclass
class Config:
    api: APIConfig = field(default_factory=APIConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    postgres_db: PostgresConfig = field(default_factory=PostgresConfig)
    event_bus: EventBusConfig = field(default_factory=EventBusConfig)
    mongo: MongoConfig = field(default_factory=MongoConfig)
