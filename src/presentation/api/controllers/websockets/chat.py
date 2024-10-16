from uuid import UUID

from fastapi import Depends, WebSocketDisconnect
from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket
from punq import Container

from src.application.messages.websockets.managers import WebSocketConnectionManager
from src.infrastructure.containers import init_container


ws_chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@ws_chat_router.websocket("/{chat_id}")
async def websocket_endpoint(
    chat_id: UUID,
    websocket: WebSocket,
    container: Container = Depends(init_container),
) -> None:
    connection_manager: WebSocketConnectionManager = container.resolve(WebSocketConnectionManager)

    await connection_manager.accept_connection(websocket, str(chat_id))

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await connection_manager.close_connection(websocket=websocket, key=str(chat_id))
