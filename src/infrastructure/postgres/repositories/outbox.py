from sqlalchemy.exc import SQLAlchemyError

from src.application.common.exceptions import OutboxError
from src.application.common.interfaces.outbox import OutboxRepo
from src.domain.common.events.event import Event
from src.infrastructure.postgres.converters import (
    convert_events_to_outbox_db_model,
)
from src.infrastructure.postgres.repositories.base import SQLAlchemyRepo
from src.infrastructure.postgres.utility_wrappers import exception_mapper


class OutboxRepoImpl(SQLAlchemyRepo, OutboxRepo):
    @exception_mapper
    async def save(self, event: Event | list[Event]) -> None:
        self._session.add_all(convert_events_to_outbox_db_model(event))
        try:
            await self._session.flush()
        except SQLAlchemyError as err:
            raise OutboxError from err
