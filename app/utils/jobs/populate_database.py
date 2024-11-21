from pymongo.mongo_client import MongoClient
import fastf1
from dotenv import load_dotenv
import os
from pprint import pprint
from ..scrapers.scrape_teams import scrape_teams
from .data_fetch.populate_teams import load_teams
load_dotenv()

MONGODB_URL = os.getenv("MONGO_DB_CONNECT")
client = MongoClient(MONGODB_URL)

connected = False

try:
    client.admin.command("ping")
    connected = True
    print("Connected to MongoDB")
except Exception as e:
    print("Failed to connect to MongoDB")
    print(e)
    
if connected:
    db = client.get_database("pitstat")
    teams = load_teams()

    try:
        db.drop_collection("teams")
        db.create_collection("teams")   
        db.teams.insert_many(teams)
        print("Teams inserted to db")
    except Exception as e:
        print("Failed to insert teams to db")
        print(e)