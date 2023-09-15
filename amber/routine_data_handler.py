import schedule
import asyncio
from .api import get_dummy_data


class RoutineDataHandler():
    routines = None

    def __init__(self) -> None:
        self.routines = get_dummy_data()
        schedule.every(1).day.do(self.reload)
        asyncio.create_task(self.reload_scheduler())

    def reload(self):
        self.routines = get_dummy_data()

    async def reload_scheduler(self):
        while True:
            schedule.run_pending()
            await asyncio.sleep(60)  # Sleep for 1 second


routineDataHandler = RoutineDataHandler()
