from sqlite3 import Date
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import random
import requests

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

db_spacex = []
db_local = []


class Data(BaseModel):
    id: int;
    name: str;
    day_of_launch: str;
    mission_name: str;
    mission_id: str;

@app.get("/")
def helloSpaceX():
  return {"message": "Hello SpaceX"}

@app.get("/api/latest")
def get_latest_launch():
    r = requests.get("https://api.spacexdata.com/v4/launches/latest")
    return r.json()
  
@app.get("/api/missions")
def get_all_launches():
    r = requests.get("https://api.spacexdata.com/v3/missions")
    return r.json()

@app.get("/api/local")  # get from local DB, once refreshed, everything gone
def get_data_local():
    return db_local

@app.post("/api/booking")  # book a rocket launch and store it in a db
def create_booking(data: Data):
    db_local.append(data)
    return data

@app.put("/api/booking/{id}")  # update a rocket launch and store it in the local db
def update_booking(id: str, data: Data):
    id = int(id);
    for i in range(len(db_local)):
        if db_local[i].id == id:
            db_local[i] = data;
            return {"message": "updated"}


@app.delete("/api/booking/{id}")  # delete a rocket launch from the local db
def delete_booking(id: str):
    id = int(id);
    for i in range(len(db_local)):
        if db_local[i].id == id:
            del db_local[i];
            return {"message": "deleted"}

''' HTML Responses '''
@app.get("/missions", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("mission.html", {"request": request})
  
@app.get("/bookings", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("bookings.html", {"request": request})