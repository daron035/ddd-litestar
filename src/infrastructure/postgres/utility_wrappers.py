from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any, ParamSpec, TypeVar

from sqlalchemy.exc import SQLAlchemyError

from src.application.common.exceptions import RepoError


Param = ParamSpec("Param")
ReturnType = TypeVar("ReturnType")
Func = Callable[Param, ReturnType]


def exception_mapper(
    func: Callable[Param, Coroutine[Any, Any, ReturnType]],
) -> Callable[Param, Coroutine[Any, Any, ReturnType]]:
    @wraps(func)
    async def wrapped(*args: Param.args, **kwargs: Param.kwargs) -> ReturnType:
        try:
            return await func(*args, **kwargs)
        except SQLAlchemyError as err:
            raise RepoError from err

    return wrapped


def close_session(func: Func) -> Func:
    @wraps(func)
    async def wrapper(self: Any, *args: Param.args, **kwargs: Param.kwargs) -> object:
        try:
            return await func(self, *args, **kwargs)
        finally:
            await self.uow.close()

    return wrapper
