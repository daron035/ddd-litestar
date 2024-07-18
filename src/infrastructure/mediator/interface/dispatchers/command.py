from typing import Any, Protocol, TypeVar

from src.infrastructure.mediator.interface.dispatchers.request import Dispatcher
from src.infrastructure.mediator.interface.entities.command import Command
from src.infrastructure.mediator.interface.handlers.command import CommandHandlerType

# from src.application.common.mediator.interface.dispatchers.request import Dispatcher
# from src.application.common.mediator.interface.entities import Command
# from src.application.common.mediator.interface.handlers import CommandHandlerType


C = TypeVar("C", bound=Command[Any])
CRes = TypeVar("CRes")


class CommandDispatcher(Dispatcher, Protocol):
    def register_handler(self, command: type[C], handler: CommandHandlerType[C, CRes]) -> None:
        raise NotImplementedError

    async def send(self, command: Command[CRes], *args: Any, **kwargs: Any) -> CRes:
        raise NotImplementedError
