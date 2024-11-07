from fastapi import APIRouter, HTTPException
# import fastf1

router = APIRouter()

@router.get("/drivers")
async def read_drivers():
    print("Reading drivers")

    return [
        {"name": "John Doe", "id": 1},
        {"name": "Alice", "id": 2},
    ]
    
@router.get("/drivers/{driver_id}")
def read_driver(driver_id: int):
    if driver_id == 1:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": "John Doe", "id": driver_id}