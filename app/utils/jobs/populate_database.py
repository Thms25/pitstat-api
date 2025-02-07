from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

from .data_fetch.populate_teams import load_teams
from .data_fetch.populate_drivers import load_drivers
from ..scrapers.scrape_past_results import get_past_data
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

    try:
        teams = load_teams()  
        db.drop_collection("teams")
        db.create_collection("teams")   
        db.teams.insert_many(teams)
        print("Teams inserted to db")
    except Exception as e:
        print("Failed to insert teams to db")
        print(e)
        
    try:
        drivers = load_drivers()
        db.drop_collection("drivers")
        db.create_collection("drivers")
        db.drivers.insert_many(drivers)
        print("Drivers inserted to db")
    except Exception as e:
        print("Failed to insert drivers to db")
        print(e)
    
    try:
        db.drop_collection("archives")
        db.create_collection("archives")
        years = ['2019', '2020', '2021', '2022', '2023', '2024']
        data = []
        for year in years:
            past_data = get_past_data(year)
            data.append(past_data)
            print(f"Inserted {year} data to db")
        db.archives.insert_many(data)
    except Exception as e:
        print("Failed to insert past data to db")
        print(e)