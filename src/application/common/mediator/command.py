from abc import abstractmethod
from collections.abc import Iterable
from typing import Protocol

from src.application.common.command import C_contra, Command, CommandHandler, CRes_co


class CommandMediator(Protocol[C_contra, CRes_co]):
    @abstractmethod
    def register_command(
        self,
        command: C_contra,
        command_handlers: Iterable[CommandHandler],
    ) -> None: ...

    @abstractmethod
    async def send(self, command: Command) -> CRes_co: ...
