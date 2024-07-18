from dataclasses import dataclass, field
from uuid import UUID

from src.domain.common.value_objects.base import ValueObject
from uuid6 import uuid7


@dataclass(frozen=True)
class Id(ValueObject[UUID]):
    value: UUID = field(init=False, kw_only=True, default_factory=uuid7)
