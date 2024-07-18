import abc
from collections.abc import Awaitable, Callable
from typing import Any, Generic, TypeVar

from src.infrastructure.mediator.interface.entities.request import Request


RRes = TypeVar("RRes")
R = TypeVar("R", bound=Request[Any])


class Handler(abc.ABC, Generic[R, RRes]):
    @abc.abstractmethod
    async def __call__(self, request: R) -> RRes:
        raise NotImplementedError


HandlerType = type[Handler[R, RRes]] | Callable[..., Awaitable[RRes]]
