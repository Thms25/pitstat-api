from fastapi import APIRouter, HTTPException
import fastf1
import datetime

router = APIRouter()

@router.get("/drivers")
async def read_drivers():
    print("Reading drivers")
    today = datetime.date.today()
    year = today.year

    calendar = fastf1.get_event_schedule(year, include_testing=False, backend=None, force_ergast=False).to_dict()

    for event in calendar['EventName']:
        race_event = fastf1.get_session(year, event, 'R', backend=None, force_ergast=False)
        print('---')
        # session = race_event.get_race()
        # print(session)

    return [
        {"name": "Lewis Hamilton", "id": 44},
        {"name": "Valtteri Bottas", "id": 77},
        {"name": "Max Verstappen", "id": 33},
        {"name": "Sergio Perez", "id": 11},
        {"name": "Daniel Ricciardo", "id": 3},
        {"name": "Lando Norris", "id": 4},
        {"name": "Charles Leclerc", "id": 16},
        {"name": "Carlos Sainz", "id": 55},
    ]

    
@router.get("/drivers/{driver_id}")
def read_driver(driver_id: int):
    if driver_id == 1:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": "John Doe", "id": driver_id}