from typing import Any, TypeVar

from src.infrastructure.mediator.dispatchers.request import DispatcherImpl
from src.infrastructure.mediator.interface.dispatchers.command import CommandDispatcher
from src.infrastructure.mediator.interface.entities.command import Command
from src.infrastructure.mediator.interface.exceptions import CommandHandlerNotFound, HandlerNotFound
from src.infrastructure.mediator.interface.handlers.request import HandlerType

# from src.application.common.mediator.dispatchers.request import DispatcherImpl
# from src.application.common.mediator.interface.dispatchers import CommandDispatcher
# from src.application.common.mediator.interface.entities import Command
# from src.application.common.mediator.interface.exceptions import CommandHandlerNotFound, HandlerNotFound
# from src.application.common.mediator.interface.handlers import HandlerType


CRes = TypeVar("CRes")
C = TypeVar("C", bound=Command[Any])


class CommandDispatcherImpl(DispatcherImpl, CommandDispatcher):
    def register_handler(self, command: type[C], handler: HandlerType[C, CRes]) -> None:
        super()._register_handler(command, handler)

    async def send(self, command: Command[CRes], *args: Any, **kwargs: Any) -> CRes:
        try:
            return await self._handle(command, *args, **kwargs)
        except HandlerNotFound as err:
            raise CommandHandlerNotFound(
                f"Command handler for {type(command).__name__} command is not registered", command,
            ) from err
