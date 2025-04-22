from fastapi import FastAPI, HTTPException
from mongita import MongitaClientDisk
from pydantic import BaseModel

class CarPool(BaseModel):
    name: str
    no_of_seats: int
    id: int

app = FastAPI()

client = MongitaClientDisk()
db = client.db
carpools = db.carpools

@app.get("/")
async def root():
    return {"message": "Hello CarPool"}

@app.get("/carpools")
async def get_carpools():
    existing_carpool = carpools.find({})
    print({"existing_carpool": existing_carpool})
    return [
        {key:carpool[key] for key in carpool if key != "_id"}
        for carpool in existing_carpool
    ]

@app.get("/carpools{carpool_id}")
async def get_carpool_by_id(carpool_id: int):
    if carpools.count_documents({"id": carpool_id}) > 0:
        carpool = carpools.find_one({"id": carpool_id})
        return {key:carpool[key] for key in carpool if key != "_id"}
    raise HTTPException(status_code=404, detail=f"No carpool with id {carpool_id} found")

@app.post("/carpools")
async def post_carpool(carpool: CarPool):
    carpools.insert_one(carpool.model_dump())
    return carpool
