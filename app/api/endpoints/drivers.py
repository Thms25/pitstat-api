from fastapi import APIRouter
# import fastf1
# import datetime
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

@router.get("/drivers")
async def read_drivers():
    return await get_mongo_drivers()

    
@router.get("/drivers/{driver_id}")
async def read_driver(driver_id: str):
    drivers = await get_mongo_drivers()
    driver = next((d for d in drivers if d['number'] == driver_id), None)
    if not driver:
        return {"driver_id": driver_id, "error": "No driver with that number"}
    return driver