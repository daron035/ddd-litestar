from dataclasses import dataclass
from uuid import UUID

from src.application.common.exceptions import ApplicationError


@dataclass(eq=False)
class ChatWithThatTitleAlreadyExistsError(ApplicationError):
    error_message: str

    @property
    def title(self) -> str:
        return f'A chat with this name "{self.error_message}" already exists.'


@dataclass(eq=False)
class ChatNotFoundError(ApplicationError):
    chat_id: UUID

    @property
    def title(self) -> str:
        return f'A chat with "{self.chat_id}" chat_id doesn\'t exist'
