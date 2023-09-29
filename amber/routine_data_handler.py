import schedule
import asyncio
from .api import get_routines_dataframe


class RoutineDataHandler():
    routines = None

    def __init__(self) -> None:
        self.routines = get_routines_dataframe()
        schedule.every(1).day.do(self.reload)
        asyncio.create_task(self.reload_scheduler())

    def reload(self):
        self.routines = get_routines_dataframe()

    async def reload_scheduler(self):
        while True:
            schedule.run_pending()
            await asyncio.sleep(60)  # Sleep for 1 second


routineDataHandler = RoutineDataHandler()
