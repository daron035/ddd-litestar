from typing import Any, Protocol, TypeVar

from src.infrastructure.mediator.interface.entities.request import Request
from src.infrastructure.mediator.interface.handlers.request import HandlerType
from src.infrastructure.mediator.middlewares.base import MiddlewareType


Self = TypeVar("Self", bound="Dispatcher")
R = TypeVar("R", bound=Request[Any])
RRes = TypeVar("RRes")


class Dispatcher(Protocol):
    @property
    def handlers(self) -> dict[type[Request[Any]], HandlerType[Request[Any], Any]]:
        raise NotImplementedError

    @property
    def middlewares(self) -> tuple[MiddlewareType[Request[Any], Any], ...]:
        raise NotImplementedError

    def copy(self: Self) -> Self:
        raise NotImplementedError
