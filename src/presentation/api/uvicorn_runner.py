import asyncio

from src.presentation.api.__main__ import main as run_app


def start_uvicorn():  # noqa
    asyncio.run(run_app())
