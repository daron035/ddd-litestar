from abc import abstractmethod
from typing import Protocol

import sqlalchemy as sa

from src.infrastructure.postgres.repositories.base import SQLAlchemyRepo
from src.infrastructure.postgres.utility_wrappers import exception_mapper


class PgHealthCheck(Protocol):
    @abstractmethod
    async def check(self) -> dict[str, bool]:
        raise NotImplementedError


class PostgresHealthcheckService(SQLAlchemyRepo, PgHealthCheck):
    @exception_mapper
    async def check(self) -> dict[str, bool]:
        cursor = await self._session.execute(sa.select(1))
        result = cursor.scalar()
        return {self.__class__.__name__: result == 1}