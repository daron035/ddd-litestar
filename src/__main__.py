import multiprocessing

import uvicorn

from apscheduler.schedulers.background import BackgroundScheduler

from src.presentation.api.main import config
from src.presentation.api.uvicorn_runner import start_uvicorn


def regular_function():  # noqa
    print("Send to outbox")


def main():  # noqa
    if config.api.debug is True:
        scheduler = BackgroundScheduler()
        scheduler.add_job(regular_function, "interval", seconds=5, max_instances=1)
        scheduler.start()

        uvicorn.run("src.presentation.api.main:init_api", reload=True, factory=True)
    else:
        app_process = multiprocessing.Process(target=start_uvicorn)
        app_process.start()

        scheduler = BackgroundScheduler()
        scheduler.add_job(regular_function, "interval", seconds=5, max_instances=1)
        scheduler.start()

        app_process.join()


if __name__ == "__main__":
    main()
