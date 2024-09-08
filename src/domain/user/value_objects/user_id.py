from dataclasses import dataclass, field
from uuid import UUID

from uuid6 import uuid7

from src.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class UserId(ValueObject[UUID]):
    value: UUID = field(default_factory=uuid7)
