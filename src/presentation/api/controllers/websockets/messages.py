from uuid import UUID

from litestar import WebSocket, websocket
from litestar.di import Provide
from punq import Container

from src.application.messages.websockets.managers import WebSocketConnectionManager
from src.infrastructure.containers import init_container
from src.infrastructure.message_broker.interface import MessageBroker
from src.infrastructure.message_broker.kafka import KafkaMessageBroker


@websocket(
    path="/chat/{chat_id:uuid}",
    dependencies={"container": Provide(init_container, sync_to_thread=False)},
)
async def websocket_endpoint(chat_id: UUID, socket: WebSocket, container: Container) -> None:
    connection_manager: WebSocketConnectionManager = container.resolve(WebSocketConnectionManager)
    message_broker: KafkaMessageBroker = container.resolve(MessageBroker)

    await connection_manager.accept_connection(socket, chat_id)

    try:
        while True:
            data = await socket.receive_text()
            print(f"Received message: {data}")

            await socket.send_text(f"Echo: {data}")
    except Exception as e:
        print(f"WebSocket connection error: {e}")
    finally:
        await connection_manager.close_connection(socket, chat_id)
