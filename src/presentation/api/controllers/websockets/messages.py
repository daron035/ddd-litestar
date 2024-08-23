from uuid import UUID

from litestar import WebSocket, websocket
from litestar.di import Provide
from litestar.exceptions import WebSocketDisconnect
from punq import Container

from src.application.messages.websockets.managers import WebSocketConnectionManager
from src.infrastructure.containers import init_container


@websocket(
    path="/chat/{chat_id:uuid}",
    dependencies={"container": Provide(init_container, sync_to_thread=False)},
)
async def websocket_endpoint(chat_id: UUID, socket: WebSocket, container: Container) -> None:
    connection_manager: WebSocketConnectionManager = container.resolve(WebSocketConnectionManager)

    await connection_manager.accept_connection(socket, str(chat_id))

    try:
        while True:
            await socket.receive_text()
    except WebSocketDisconnect:
        await connection_manager.close_connection(websocket=socket, key=str(chat_id))
