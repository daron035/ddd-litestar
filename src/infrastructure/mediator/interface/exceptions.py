from typing import Any

from src.infrastructure.mediator.interface.entities.command import Command
from src.infrastructure.mediator.interface.entities.query import Query
from src.infrastructure.mediator.interface.entities.request import Request


class MediatorError(Exception):
    pass


class HandlerNotFoundError(MediatorError, TypeError):
    request: Request[Any]

    def __init__(self, text: str, request: Request[Any]):
        super().__init__(text)
        self.request = request


class CommandHandlerNotFoundError(HandlerNotFoundError):
    request: Command[Any]


class QueryHandlerNotFoundError(HandlerNotFoundError):
    request: Query[Any]
