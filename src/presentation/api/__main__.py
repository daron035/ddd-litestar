import asyncio

from src.infrastructure.config import config
from src.presentation.api.main import init_api, run_api


async def main() -> None:
    app = init_api()
    await run_api(app, config.api)


if __name__ == "__main__":
    asyncio.run(main())
