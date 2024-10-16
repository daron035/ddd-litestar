import logging

from typing import Any

from fastapi import APIRouter, Depends, status
from fastapi.responses import PlainTextResponse
from punq import Container

from src.infrastructure.containers import init_container
from src.infrastructure.postgres.services.healthcheck import PgHealthCheck


logger = logging.getLogger(__name__)


general_router = APIRouter(
    tags=["general"],
)


@general_router.get(
    "/test-pg-connection",
    status_code=status.HTTP_200_OK,
)
async def test_postgres_db(
    container: Container = Depends(init_container),
) -> Any:
    psql: PgHealthCheck = container.resolve(PgHealthCheck)
    response = await psql.check()
    return response


@general_router.get("/books/{book_id}", response_model=dict)
async def get_book(book_id: int) -> dict[str, int]:
    return {"book_id": book_id}


@general_router.get("/healthcheck", response_class=PlainTextResponse)
async def healthcheck() -> str:
    return "healthy"
