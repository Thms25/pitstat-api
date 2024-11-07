from fastapi import APIRouter
import fastf1

router = APIRouter()

@router.get("/races")
async def read_races(year: int = 2024):
    
    print(f"Fetching calendar for {year}")
    calendar = fastf1.get_event_schedule(year, include_testing=False, backend=None, force_ergast=False)
    return calendar.to_dict(orient='records')

@router.get("/races/{round}")
async def read_race(round: int, year: int = 2024):
    races = fastf1.get_event_schedule(year, include_testing=False, backend=None, force_ergast=False)
    race = races.get_event_by_round(round)
    return race.to_dict()