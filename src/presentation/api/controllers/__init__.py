from src.presentation.api.controllers.websockets.messages import websocket_endpoint

from .controllers import (
    create_chat,
    create_message,
    create_user,
    get_book,
    get_chat_messages,
    health_check,
    test_postgres_db,
)


controllers = [
    create_chat,
    create_message,
    get_chat_messages,
    get_book,
    health_check,
    websocket_endpoint,
    test_postgres_db,
    create_user,
]
