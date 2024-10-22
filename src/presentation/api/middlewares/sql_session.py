from collections.abc import Awaitable, Callable

from fastapi import Request, Response

from src.application.common.interfaces.uow import UnitOfWork
from src.infrastructure.containers import init_container


async def sql_session_close(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    response = await call_next(request)
    uow: UnitOfWork = init_container().resolve(UnitOfWork)
    await uow.close()
    return response
