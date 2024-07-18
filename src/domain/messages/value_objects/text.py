from dataclasses import dataclass

from src.domain.common.exceptions.base import DomainError
from src.domain.common.value_objects import ValueObject


MAX_TEXT_LENGTH = 1000


@dataclass(eq=False)
class WrongTextValueError(ValueError, DomainError):
    text: str

    @property
    def title(self) -> str:
        return self.text


class EmptyTextError(WrongTextValueError):
    @property
    def title(self) -> str:
        return "Text can't be empty"


class TooLongTextError(WrongTextValueError):
    @property
    def title(self) -> str:
        return f'Too long text "{self.text}[:20]..."'


@dataclass(frozen=True)
class Text(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if len(self.value) == 0:
            raise EmptyTextError(self.value)
        if len(self.value) > MAX_TEXT_LENGTH:
            raise TooLongTextError(self.value)
