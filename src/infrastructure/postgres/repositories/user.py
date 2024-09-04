import sqlalchemy as sa

from src.application.user.intefraces.persistence.repo import PostgresRepo
from src.infrastructure.postgres.exception_mapper import close_session
from src.infrastructure.postgres.repositories.base import SQLAlchemyRepo


class PostgresRepoImpl(SQLAlchemyRepo, PostgresRepo):
    @close_session
    async def check(self) -> None:
        cursor = await self._session.execute(sa.select(1))
        result = cursor.scalar()
        # return

    # # contextmanager()
    # async def ae(self):
    #     async with self._session as session:
    #         cursor = await session.execute(sa.select(1))
    #         result = cursor.scalar()
    #         return {self.__class__.__name__: result == 1}
