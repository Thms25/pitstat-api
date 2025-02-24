from fastapi import APIRouter
# import fastf1
import datetime
from app.database.connection import connect

router = APIRouter()
async def get_mongo_drivers():
    client = await connect()
    db = client.get_database("pitstat")
    drivers_collection = db.get_collection("drivers")
    drivers_cursor = drivers_collection.find()
    drivers = list(drivers_cursor)
    
    for driver in drivers:
        driver["_id"] = str(driver["_id"])

    return drivers

async def get_archived_drivers(year: int):
    client = await connect()
    db = client.get_database("pitstat")
    drivers_collection = db.get_collection("archives")
    drivers_cursor = drivers_collection.find()
    archives = list(drivers_cursor)
    archive = next((arc for arc in archives if arc['year'] == str(year)), None)

    if not archive:
        return {"error": "No data available for that year"}

    return archive['driver_standings']

cuurent_year = datetime.datetime.now().year
@router.get("/drivers")
async def read_drivers(year: int = cuurent_year):
    if year < 2019:
        return {"error": "No data available for year before 2019"}
    if year < cuurent_year:
        print('going to archives')
        drivers = await get_archived_drivers(year)
        return drivers
    drivers = await get_mongo_drivers()
    return sorted(drivers, key=lambda d: d['rank'])

    
@router.get("/drivers/{driver_id}")
async def read_driver(driver_id: str, year: int = cuurent_year):
    if year < 2019:
        return {"error": "No data available for year before 2019"}
    if year < cuurent_year:
        drivers = await get_archived_drivers(year)
        driver = next((d for d in drivers if d['code'] == driver_id), None)
        if not driver:
            return {"driver_id": driver_id, "error": "No driver with that number"}
        return driver

    drivers = await get_mongo_drivers()
    if driver_id.isnumeric():
        driver = next((d for d in drivers if d['number'] == int(driver_id)), None)
        return driver
    driver = next((d for d in drivers if d['id'] == driver_id), None)
    if not driver:
        return {"driver_id": driver_id, "error": "No driver with that number or id"}
    return driver