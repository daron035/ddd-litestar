from dataclasses import dataclass

from src.domain.common.exceptions.base import AppError


class ApplicationError(AppError):
    """Base Application Error."""

    @property
    def title(self) -> str:
        return "An application error occurred"


@dataclass(eq=False)
class MappingError(ApplicationError):
    _text: str

    @property
    def title(self) -> str:
        return self._text
