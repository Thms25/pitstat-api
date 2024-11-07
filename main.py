from fastapi import FastAPI
from app.api.endpoints import drivers, races

app = FastAPI()

app.include_router(drivers.router)
app.include_router(races.router)

@app.get("/")
def read_root():
    return {"Info": "This is pitstat's api"}
