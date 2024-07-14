from abc import abstractmethod
from typing import Any, Protocol, TypeVar


C_contra = TypeVar("C_contra", bound="Command", contravariant=True)
CRes_co = TypeVar("CRes_co", bound=Any, covariant=True)


class Command(Protocol): ...


class CommandHandler(Protocol[C_contra, CRes_co]):
    @abstractmethod
    async def handle(self, command: C_contra) -> CRes_co: ...
