from dataclasses import dataclass

from src.domain.common.exceptions.base import AppError


class ApplicationError(AppError):
    """Base Application Error."""

    @property
    def title(self) -> str:
        return "An application error occurred"


class UnexpectedError(ApplicationError):
    pass


class CommitError(UnexpectedError):
    pass


class SessionCloseError(UnexpectedError):
    pass


class RollbackError(UnexpectedError):
    pass


class RepoError(UnexpectedError):
    pass


@dataclass(eq=False)
class MappingError(ApplicationError):
    _text: str

    @property
    def title(self) -> str:
        return self._text
