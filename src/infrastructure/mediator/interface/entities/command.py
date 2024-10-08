import abc

from typing import Generic, TypeVar

from src.infrastructure.mediator.interface.entities.request import Request


CRes = TypeVar("CRes")


class Command(Request[CRes], abc.ABC, Generic[CRes]):
    pass
