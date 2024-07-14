from dataclasses import dataclass

from src.domain.common.exceptions import ApplicationError


@dataclass(eq=False)
class ChatWithThatTitleAlreadyExistsError(ApplicationError):
    error_message: str

    @property
    def message(self) -> str:
        return f'Чат c таким названием "{self.error_message}" уже существует.'


@dataclass(eq=False)
class ChatNotFoundError(ApplicationError):
    chat_oid: str

    @property
    def message(self) -> str:
        return "Чат c таким ID не найден."
