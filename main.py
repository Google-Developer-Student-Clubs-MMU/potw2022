from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

db_spacex = []
db_local = []


class Data(BaseModel):
    rocketName: str
    time: str


@app.get("/latest")
def get_latest_launch():
    r = requests.get("https://api.spacexdata.com/v4/launches/latest")
    return r.json()


@app.get("/local")  # get from local DB, once refreshed, everything gone
def get_data_local():
    return db_local


@app.post("/booking")  # book a rocket launch and store it in a db
def create_booking(data: Data):
    db_local.append(data)
    return data


@app.put("/booking/{id}")  # update a rocket launch and store it in the local db
def update_booking(id: int, data: Data):
    db_local[id] = data
    return data


@app.delete("/booking/{id}")  # delete a rocket launch from the local db
def delete_booking(id: int):
    del db_local[id]
    return db_local
