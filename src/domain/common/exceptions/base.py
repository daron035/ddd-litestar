from dataclasses import dataclass


@dataclass(eq=False)
class AppError(Exception):
    """Base Error."""

    @property
    def title(self) -> str:
        return "An app error occurred"


class DomainError(AppError):
    """Base Domain Error."""

    @property
    def title(self) -> str:
        return "A domain error occurred"


class ApplicationError(AppError):
    """Base Application Error."""

    @property
    def title(self) -> str:
        return "An application error occurred"
