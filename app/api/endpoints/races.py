from fastapi import APIRouter
import fastf1
import countryflag
import datetime
from app.database.connection import connect

router = APIRouter()

async def get_archived_races(year: int):
    client = await connect()
    db = client.get_database("pitstat")
    arc_collection = db.get_collection("archives")
    arc_cursor = arc_collection.find()
    archives = list(arc_cursor)
    archive = next((arc for arc in archives if arc['year'] == str(year)), None)

    if not archive:
        return {"error": "No data available for that year"}

    return archive['races_data']

async def get_schedule(year: int):
    return fastf1.get_event_schedule(year, include_testing=False, backend=None, force_ergast=False)

def clean_race_info(info):
    return {
        'round': info['RoundNumber'],
        'name': info['EventName'],
        'official_name': info['OfficialEventName'],
        'location': info['Location'],
        'country': info['Country'],
        'date': info['EventDate'],
        'status': 'completed' if info['EventDate'] < datetime.datetime.now() else 'upcoming',
        'format': info['EventFormat'],
        'flag': countryflag.getflag([info['Country']]),
    }

current_year = datetime.datetime.now().year
@router.get("/races")
async def read_races(year: int = current_year):
    if year >= 2019 and year < current_year:
        races = await get_archived_races(year)
        return races
    calendar = await get_schedule(year)
    races = calendar.to_dict(orient='records')
    clean_races = []
    for race in races:
        clean_race = clean_race_info(race)
        clean_race['results'] = []
        # race_event = calendar.get_event_by_round(race['RoundNumber'])
        # race_session = race_event.get_race()
        # race_session.load()
        clean_races.append(clean_race)
    return clean_races

@router.get("/races/{round}")
async def read_race(round: int, year: int = 2024):
    races = await get_schedule(year)
    race = races.get_event_by_round(round)
    race_info = clean_race_info(race.to_dict())
    race_session = race.get_race()
    race_session.load()
    results = []

    for n in race_session.results['DriverNumber'].keys():
        results.append({
            'driver_number': int(race_session.results['DriverNumber'][n]),
            'position': race_session.results['Position'][n],
            'grid_position': race_session.results['GridPosition'][n],
            'driver': race_session.results['FullName'][n],
            'code': race_session.results['Abbreviation'][n],
            'team': race_session.results['TeamName'][n],
            'picture': race_session.results['HeadshotUrl'][n],
            'points': race_session.results['Points'][n],
            'status': race_session.results['Status'][n],
            'driver_id': race_session.results['DriverId'][n],
            'team_id': race_session.results['TeamId'][n],
            
        })
            
    race_info['results'] = sorted(results, key=lambda r: r['position'])
    # laps = race_session.laps
    # fastest_lap = laps.pick_fastest()

    return race_info