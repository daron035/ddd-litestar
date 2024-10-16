from fastapi import FastAPI

from src.presentation.api.controllers.exceptions import setup_exception_handlers

from .chat import chat_router
from .default import default_router
from .general import general_router
from .user import user_router
from .websockets.chat import ws_chat_router


def setup_controllers(app: FastAPI) -> None:
    app.include_router(default_router)
    app.include_router(general_router)
    app.include_router(user_router)
    app.include_router(chat_router)
    app.include_router(ws_chat_router)
    setup_exception_handlers(app)
