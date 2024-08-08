from dataclasses import dataclass

from src.domain.common.exceptions.base import ApplicationError


@dataclass(eq=False)
class MappingError(ApplicationError):
    _text: str

    @property
    def title(self) -> str:
        return self._text
