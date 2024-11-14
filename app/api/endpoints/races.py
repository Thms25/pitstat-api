from fastapi import APIRouter
import fastf1
import countryflag
import datetime


router = APIRouter()

async def get_schedule(year: int):
    return fastf1.get_event_schedule(year, include_testing=False, backend=None, force_ergast=False)

@router.get("/races")
async def read_races(year: int = 2024):
    today = datetime.datetime.now()
    calendar = await get_schedule(year)
    races = calendar.to_dict(orient='records')
    for race in races:
        race['flag'] = countryflag.getflag([race['Country']])
        # race_event = calendar.get_event_by_round(race['RoundNumber'])
        # race_session = race_event.get_race()
        # race_session.load()
        race['results'] = []
        if race['EventDate'] < today:
            race['status'] = 'completed'
        else:
            race['status'] = 'upcoming'
            
        
    return races

@router.get("/races/{round}")
async def read_race(round: int, year: int = 2024):
    races = await get_schedule(year)
    race = races.get_event_by_round(round)
    info = race.to_dict()
    race_session = race.get_race()
    race_session.load()
    flag = countryflag.getflag([info['Country']])
    info['flag'] = flag
    results = race_session.results
    laps = race_session.laps
    fastest_lap = laps.pick_fastest()

    return {
        "info": info,
        "results": results.to_dict(orient='records'),
        "fastest_lap": fastest_lap.to_dict()
        }