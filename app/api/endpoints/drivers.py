from fastapi import APIRouter, HTTPException
import fastf1
import datetime
from app.utils.scrapers.scrape_drivers import scrape_drivers
from pprint import pprint

router = APIRouter()

@router.get("/drivers")
async def read_drivers():
    scraped_drivers = scrape_drivers()
    print("Reading drivers")

    return scraped_drivers

    
@router.get("/drivers/{driver_id}")
def read_driver(driver_id: int):
    # schedule = fastf1.get_event_schedule(2024, include_testing=False, backend=None, force_ergast=False)
    # last_event = schedule.get_event_by_round(21)
    # race_session = last_event.get_race()
    # print(race_session)
    # race_session.load()
    # print(race_session.results)
    # scraped_drivers = scrape_drivers()
    # driver = scraped_drivers[0]
    # return driver
    return {"driver_id": driver_id}