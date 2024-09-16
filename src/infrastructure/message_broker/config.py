from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class EventBusConfig:
    bootstrap_servers: str = "localhost:29092"
    group_id: str = f"chats-{uuid4()}"
    metadata_max_age_ms: int = 30000
