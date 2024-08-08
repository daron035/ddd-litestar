from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Message:
    topic: str
    key: bytes
    value: bytes
    headers: list[tuple[str, bytes]] | None
