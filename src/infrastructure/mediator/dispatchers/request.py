import abc

from collections.abc import Awaitable, Callable, Sequence
from typing import Any, TypeVar

from src.infrastructure.mediator.interface.dispatchers.request import Dispatcher
from src.infrastructure.mediator.interface.entities.request import Request
from src.infrastructure.mediator.interface.exceptions import HandlerNotFoundError
from src.infrastructure.mediator.interface.handlers.request import HandlerType
from src.infrastructure.mediator.middlewares.base import Middleware, MiddlewareType, wrap_middleware


Self = TypeVar("Self", bound="DispatcherImpl")
RRes = TypeVar("RRes")
R = TypeVar("R", bound=Request[Any])
Middlewares = Sequence[MiddlewareType[Request[Any], Any]]
Handlers = dict[type[Request[Any]], HandlerType[Request[Any], Any]]

DEFAULT_MIDDLEWARES: tuple[MiddlewareType[Request[Any], Any], ...] = (Middleware(),)


class DispatcherImpl(Dispatcher, abc.ABC):
    def __init__(
        self,
        middlewares: Middlewares = (),
        *,
        handlers: Handlers | None = None,
    ) -> None:
        self._middlewares = middlewares

        if handlers is None:
            handlers = {}
        self._handlers = handlers

    @property
    def handlers(self) -> Handlers:
        return self._handlers

    @property
    def middlewares(self) -> tuple[MiddlewareType[Request[Any], Any], ...]:
        return tuple(self._middlewares)

    def copy(self: Self) -> Self:
        return self.__class__(self._middlewares, handlers=self._handlers)

    def _register_handler(self, request: type[R], handler: HandlerType[R, RRes]) -> None:
        self._handlers[request] = handler

    async def _handle(self, request: Request[RRes], *args: Any, **kwargs: Any) -> RRes:
        try:
            handler = self._handlers[type(request)]
        except KeyError as err:
            raise HandlerNotFoundError(
                f"Request handler for {type(request).__name__} request is not registered",
                request,
            ) from err

        # Handler has to be wrapped with at least one middleware to initialize the handler if it is necessary
        middlewares: Middlewares = self._middlewares if self._middlewares else DEFAULT_MIDDLEWARES
        wrapped_handler: Callable[..., Awaitable[RRes]] = self._wrap_middleware(middlewares, handler)
        return await wrapped_handler(request, *args, **kwargs)

    @staticmethod
    def _wrap_middleware(
        middlewares: Sequence[MiddlewareType[R, Any]],
        handler: HandlerType[R, Any],
    ) -> Callable[..., Awaitable[Any]]:
        return wrap_middleware(middlewares, handler)
