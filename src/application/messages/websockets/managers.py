from abc import abstractmethod
from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Protocol
from uuid import UUID

from litestar import WebSocket


@dataclass
class Connections:
    connections_map: dict[UUID, list[WebSocket]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )


class WebSocketConnectionManager(Protocol):
    @abstractmethod
    async def accept_connection(self, websocket: WebSocket, key: UUID) -> None:
        ...

    @abstractmethod
    async def close_connection(self, websocket: WebSocket, key: UUID) -> None:
        ...

    @abstractmethod
    async def send_all(self, key: UUID, json_message: Mapping[UUID, Any]) -> None:
        ...


@dataclass
class ConnectionManager(Connections, WebSocketConnectionManager):
    async def accept_connection(self, websocket: WebSocket, key: UUID) -> None:
        await websocket.accept()
        self.connections_map[key].append(websocket)

    async def close_connection(self, websocket: WebSocket, key: UUID) -> None:
        await websocket.close()
        self.connections_map[key].remove(websocket)

    async def send_all(self, key: UUID, json_message: Mapping[UUID, Any]) -> None:
        for websocket in self.connections_map[key]:
            # await websocket.send_json(json_message)
            await websocket.send_text("oiqwueioqwueroip")
