from dataclasses import dataclass
from uuid import UUID

from src.domain.common.exceptions import DomainError


@dataclass(eq=False)
class ListenerAlreadyExistsError(DomainError):
    listener_id: UUID

    @property
    def title(self) -> str:
        return f'Listener with "{self.listener_id}" id already listens this chat.'
