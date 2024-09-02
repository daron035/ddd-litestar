from typing import Protocol

import sqlalchemy as sa

from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session


def close_session(method):
    async def wrapper(self, *args, **kwargs):
        try:
            return await method(self, *args, **kwargs)
        finally:
            if self._session:
                await self._session.close()
                print(f"Сессия закрыта для метода {method.__name__}")
    return wrapper


class PostgresRepo(Protocol):
    async def check(self) -> None:
        raise NotImplementedError


class PostgresRepoImpl(SQLAlchemyRepo, PostgresRepo):
    @close_session
    async def check(self) -> None:
        print("self._session")
        print(self._session)
        cursor = await self._session.execute(sa.select(1))
        result = cursor.scalar()
        print({self.__class__.__name__: result == 1})

    # # contextmanager()
    # async def ae(self):
    #     async with self._session as session:
    #         print("self._session")
    #         print(session)
    #         cursor = await session.execute(sa.select(1))
    #         result = cursor.scalar()
    #         return {self.__class__.__name__: result == 1}
