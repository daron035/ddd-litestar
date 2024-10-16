from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import orjson

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.infrastructure.postgres.config import PostgresConfig


async def build_sa_engine(db_config: PostgresConfig) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        db_config.full_url,
        echo=True,
        echo_pool=db_config.echo,
        json_serializer=lambda data: orjson.dumps(data).decode(),
        json_deserializer=orjson.loads,
        pool_size=50,
    )
    yield engine

    await engine.dispose()


def build_sa_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    session_factory = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    return session_factory


async def build_sa_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


class PostgresManager:
    def __init__(self, db_config: PostgresConfig):
        self._db_config = db_config
        self._async_engine = create_async_engine(
            self._db_config.full_url,
            echo=True,
            echo_pool=self._db_config.echo,
            json_serializer=lambda data: orjson.dumps(data).decode(),
            json_deserializer=orjson.loads,
            pool_size=50,
            isolation_level="READ COMMITTED",
        )
        self._read_only_async_engine = create_async_engine(
            self._db_config.full_url,
            echo=True,
            echo_pool=self._db_config.echo,
            json_serializer=lambda data: orjson.dumps(data).decode(),
            json_deserializer=orjson.loads,
            pool_size=50,
            isolation_level="AUTOCOMMIT",
        )
        self.read_only_session_factory = async_sessionmaker(
            bind=self._read_only_async_engine,
            autoflush=False,
            expire_on_commit=False,
        )
        self.session_factory = async_sessionmaker(bind=self._async_engine, autoflush=False, expire_on_commit=False)

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        session: AsyncSession = self.session_factory()
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.commit()
            await session.close()

    @asynccontextmanager
    async def get_read_only_session(self) -> AsyncGenerator[AsyncSession, None]:
        session: AsyncSession = self.read_only_session_factory()
        try:
            yield session
        except SQLAlchemyError:
            raise
        finally:
            await session.close()
