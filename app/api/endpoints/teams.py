from fastapi import APIRouter
from app.database.connection import connect
import datetime

router = APIRouter()

async def get_mongo_teams():
    client = await connect()
    db = client.get_database("pitstat")
    team_collection = db.get_collection("teams")
    teams_cursor = team_collection.find()
    teams = list(teams_cursor)
    
    for team in teams:
        team["_id"] = str(team["_id"])

    return teams

async def get_archived_teams(year: int):
    client = await connect()
    db = client.get_database("pitstat")
    arc_collection = db.get_collection("archives")
    arc_cursor = arc_collection.find()
    archives = list(arc_cursor)
    archive = next((arc for arc in archives if arc['year'] == str(year)), None)

    if not archive:
        return {"error": "No data available for that year"}

    return archive['constructor_standings']

current_year = datetime.datetime.now().year
@router.get("/teams")
async def read_teams(year: int = current_year):
    if year < 2019:
        return {"error": "No data available for year before 2019"}
    if year < current_year:
        teams = await get_archived_teams(year)
        return teams
    return await get_mongo_teams()

    
@router.get("/teams/{team_id}")
async def read_team(team_id: str, year: int = current_year):
    if year < 2019:
        return {"error": "No data available for year before 2019"}
    if year < current_year:
        teams = await get_archived_teams(year)
        team = next((team for team in teams if team['name'].lower() == team_id.lower()), None)
        if team:
            return team
        return {"team_id": team_id, "error": "Team not found"}
    teams = await get_mongo_teams()
    team = next((team for team in teams if team['id'] == team_id.lower()), None)
    if team:
        return team
    return {"team_id": team_id, "error": "Team not found"}
