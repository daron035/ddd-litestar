from dataclasses import dataclass

from src.domain.common.exceptions import DomainError


@dataclass(eq=False)
class ListenerAlreadyExistsError(DomainError):
    listener_oid: str

    @property
    def title(self) -> str:
        return f'Listener with "{self.listener_oid}" id already listens this chat.'
