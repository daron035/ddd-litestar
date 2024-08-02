from dataclasses import dataclass, field

from src.infrastructure.message_broker.config import EventBusConfig
from src.infrastructure.mongo.config import MongoConfig


@dataclass
class APIConfig:
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = __debug__


@dataclass
class Config:
    api: APIConfig = field(default_factory=APIConfig)
    mongo: MongoConfig = field(default_factory=MongoConfig)
    event_bus: EventBusConfig = field(default_factory=EventBusConfig)
