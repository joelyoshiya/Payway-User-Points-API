import datetime
from typing import Dict
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserRoute(str, Enum):
    add = "add"
    spend = "spend"
    points = "points"


class Payer(str,Enum):
    dannon = 'DANNON'
    unilever = 'UNILEVER'
    miller_coors = 'MILLER COORS'


class Transaction(BaseModel):
    payer: Payer
    points: int
    timestamp: datetime.datetime

    # TODO create a validator checking for specific date format
    # use pre-validator


class Spend(BaseModel):
    points: int

class SpendResponse(BaseModel):
    payer: Payer
    points: int

class balanceResponse(BaseModel):
    __root__: Dict[Payer, int]

@app.get("/")
async def root():
    return {"message": "wassup big stepper"}

@app.get("/status")
async def status():
    return {"status": "web server working"}

# return the user id and their points balance
@app.get("/users/{user_id}")
async def read_item(user_id: str):
    return {"user_id": user_id, "points": 100}

# @app.post("/transactions/")
# async def create_transaction(transaction: Transaction):
#     return transaction

# handles all the operations on the user's points balance
@app.get("/users/{user_id}: str/{user_route}")
async def get_route(user_route: UserRoute, user_id: str):
    if user_route == UserRoute.add:
        return {"model_name": user_route, "user_id": user_id, "message": "going to add a transaction"}

    if user_route.value == "spend":
        return {"model_name": user_route, "user_id": user_id, "message": "going to spend points"}

    return {"user_route": user_route, "user_id": user_id, "message": "going to  return points balance"}