from dataclasses import dataclass

from src.domain.common.exceptions.base import DomainError
from src.domain.common.value_objects import ValueObject


MAX_TITLE_LENGTH = 255


@dataclass(eq=False)
class WrongTitleValueError(ValueError, DomainError):
    wrong_title: str


class EmptyTitleError(WrongTitleValueError):
    @property
    def title(self) -> str:
        return "Title can't be empty"


class TooLongTitleError(WrongTitleValueError):
    @property
    def title(self) -> str:
        return f'Too long text "{self.wrong_title}"'


@dataclass(frozen=True)
class Title(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if len(self.value) == 0:
            raise EmptyTitleError(self.value)
        if len(self.value) > MAX_TITLE_LENGTH:
            raise TooLongTitleError(self.value)
