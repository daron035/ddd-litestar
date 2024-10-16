from abc import abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Protocol

from fastapi.websockets import WebSocket


@dataclass
class Connections:
    connections_map: dict[str, list[WebSocket]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )


class WebSocketConnectionManager(Protocol):
    @abstractmethod
    async def accept_connection(self, websocket: WebSocket, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close_connection(self, websocket: WebSocket, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def send_all(self, key: str, bytes_: bytes) -> None:
        raise NotImplementedError


@dataclass
class ConnectionManager(Connections, WebSocketConnectionManager):
    async def accept_connection(self, websocket: WebSocket, key: str) -> None:
        await websocket.accept()
        self.connections_map[key].append(websocket)

    async def close_connection(self, websocket: WebSocket, key: str) -> None:
        await websocket.close()
        self.connections_map[key].remove(websocket)

    async def send_all(self, key: str, bytes_: bytes) -> None:
        for websocket in self.connections_map[key]:
            await websocket.send_bytes(bytes_)
