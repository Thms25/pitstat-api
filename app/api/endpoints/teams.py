from fastapi import APIRouter
from app.database.connection import connect

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

@router.get("/teams")
async def read_teams():
    return await get_mongo_teams()

    
@router.get("/teams/{team_id}")
async def read_team(team_id: str):
    teams = await get_mongo_teams()
    team = next((team for team in teams if team['id'] == team_id.lower()), None)
    if team:
        return team
    return {"team_id": team_id, "error": "Team not found"}
