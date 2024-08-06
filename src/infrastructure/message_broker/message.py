from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, kw_only=True)
class Message:
    topic: str
    key: Any
    value: Any
    headers: Any
