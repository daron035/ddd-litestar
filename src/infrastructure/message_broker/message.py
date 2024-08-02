from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from uuid6 import uuid7


# @dataclass(frozen=True, kw_only=True)
# class Message:
#     id: UUID = field(default_factory=uuid7)
#     data: str = ""
#     message_type: str = "message"
    
@dataclass(frozen=True, kw_only=True)
class Message:
    topic: str
    key: Any
    value: Any
    headers: Any
    # topic: str = "test-topic"
    # key: Any = b"Yeey"
    # value: Any = b"Super-pooper message"
    # headers: Any = [("adsfasd", b"asdfsad")])
