from fastapi import APIRouter
import fastf1

router = APIRouter()

async def get_schedule(year: int):
    return fastf1.get_event_schedule(year, include_testing=False, backend=None, force_ergast=False)

@router.get("/races")
async def read_races(year: int = 2024):
    calendar = await get_schedule(year)
    return calendar.to_dict(orient='records')

@router.get("/races/{round}")
async def read_race(round: int, year: int = 2024):
    races = await get_schedule(year)
    race = races.get_event_by_round(round)
    race_session = race.get_race()
    race_session.load()
    results = race_session.results
    laps = race_session.laps
    fastest_lap = laps.pick_fastest()

    return {
        "race_info" :race.to_dict(),
        "results": results.to_dict(orient='records'),
        "fastest_lap": fastest_lap.to_dict()
        }