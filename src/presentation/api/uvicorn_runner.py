import asyncio

from src.presentation.api.__main__ import main


def start_uvicorn():  # noqa
    asyncio.run(main())
