from typing import Any

from src.infrastructure.mediator.interface.entities.command import Command
from src.infrastructure.mediator.interface.entities.query import Query
from src.infrastructure.mediator.interface.entities.request import Request

# from src.application.common.mediator.interface.entities import Command, Query, Request


class MediatorError(Exception):
    pass


class HandlerNotFound(MediatorError, TypeError):
    request: Request[Any]

    def __init__(self, text: str, request: Request[Any]):
        super().__init__(text)
        self.request = request


class CommandHandlerNotFound(HandlerNotFound):
    request: Command[Any]


class QueryHandlerNotFound(HandlerNotFound):
    request: Query[Any]
