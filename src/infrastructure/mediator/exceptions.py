from dataclasses import dataclass

from src.domain.common.exceptions.base import ApplicationError


@dataclass(eq=False)
class CommandHandlersNotRegisteredError(ApplicationError):
    command_type: type

    @property
    def message(self) -> str:
        return f"Failed to find handlers for the command: {self.command_type}"
