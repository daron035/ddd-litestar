import asyncio
import logging

from src.infrastructure.config_loader import load_config
from src.infrastructure.log.main import configure_logging
from src.presentation.api.config import Config
from src.presentation.api.main import init_api, run_api


logger = logging.getLogger(__name__)


async def main() -> None:
    config = load_config(Config)
    configure_logging(config.logging)

    logger.info("Launch app", extra={"config": config})

    app = init_api(debug=config.api.debug, log_cfg=config.logging)
    await run_api(app, config.api)


if __name__ == "__main__":
    asyncio.run(main())
