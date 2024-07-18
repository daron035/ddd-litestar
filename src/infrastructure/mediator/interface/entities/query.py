import abc
from typing import Generic, TypeVar

from src.infrastructure.mediator.interface.entities.request import Request

# from src.application.common.mediator.interface.entities.request import Request


QRes = TypeVar("QRes")


class Query(Request[QRes], abc.ABC, Generic[QRes]):
    pass
