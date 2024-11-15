from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

async def connect():
    MONGODB_URL = os.getenv("MONGO_DB_CONNECT")
    client = MongoClient(MONGODB_URL)

    try:
        client.admin.command("ping")
        print("Connected to MongoDB")
        return client
    except Exception as e:
        print("Failed to connect to MongoDB")
        print(e)
        return None
    