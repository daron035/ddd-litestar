from collections.abc import Mapping
from datetime import datetime
from enum import Enum
from uuid import UUID

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import JSON
from uuid6 import uuid7

from .base import BaseModel


class Status(Enum):
    PENDING = "pending"
    PROCESSED = "processed"


class Outbox(BaseModel):
    __tablename__ = "outbox"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7, server_default=sa.func.uuid_generate_v7())
    occurred_on: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    type: Mapped[str] = mapped_column(nullable=False)
    data: Mapped[Mapping] = mapped_column(JSON)
    status: Mapped[Status] = mapped_column(default=Status.PENDING)
    processed_on: Mapped[datetime | None]
