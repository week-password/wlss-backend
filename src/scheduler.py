from __future__ import annotations

import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.config import CONFIG
from src.file.jobs import delete_unused_files


async def main() -> None:
    scheduler = AsyncIOScheduler({"apscheduler.timezone": "UTC"})

    scheduler.add_job(delete_unused_files, "interval", minutes=CONFIG.SCHEDULER_TRIGGER_MINUTES_INTERVAL)

    scheduler.start()

    while scheduler.running:  # pylint: disable=while-used
        await asyncio.sleep(1)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
