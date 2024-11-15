from fastapi import FastAPI
from app.api.endpoints import drivers, races, teams
from contextlib import asynccontextmanager
# from app.utils.jobs.populate_database import load_data, clean_dat

@asynccontextmanager
async def lifespan(app: FastAPI):
    # await load_data()
    # await clean_data()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(drivers.router)
app.include_router(races.router)
app.include_router(teams.router)

@app.get("/")
def read_root():
    return {"Info": "This is pitstat's api"}
