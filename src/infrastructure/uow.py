from collections.abc import Sequence

from src.application.common.interfaces.uow import UnitOfWork
from src.infrastructure.postgres.uow import SQLAlchemyUoW


def build_uow(db_uow: SQLAlchemyUoW) -> UnitOfWork:
    uow = UnitOfWorkImpl((db_uow,))
    return uow


class UnitOfWorkImpl(UnitOfWork):
    def __init__(self, uows: Sequence[UnitOfWork]) -> None:
        self._uows = uows

    async def commit(self) -> None:
        for uow in self._uows:
            await uow.commit()

    async def rollback(self) -> None:
        for uow in self._uows:
            await uow.rollback()

    async def close(self) -> None:
        for uow in self._uows:
            await uow.close()
