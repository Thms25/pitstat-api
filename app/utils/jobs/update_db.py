from fastapi_utilities import repeat_every
from asyncio import sleep

@repeat_every(seconds=3)
async def load_data():
    print("\nPopulating database\n")
    await sleep(1)


@repeat_every(seconds=10)
async def clean_data():
    print("\nCleaning database\n")
    await sleep(1)