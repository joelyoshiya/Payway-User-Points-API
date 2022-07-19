import datetime
from typing import Dict
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Enum classes ---------------------------------------------------------------
# Enum class for user routes
class UserRoute(str, Enum):
    add = "add"
    spend = "spend"
    points = "points"

# Enum class for possible payers from client
class Payer(str,Enum):
    dannon = 'DANNON'
    unilever = 'UNILEVER'
    miller_coors = 'MILLER COORS'

# Pydantic models ------------------------------------------------------------

# Request Body Models ---------------------------------------------------------
class Transaction(BaseModel):
    payer: Payer
    points: int
    timestamp: datetime.datetime

    # TODO create a validator checking for specific date format
    # use pre-validator
    # see: https://pydantic-docs.helpmanual.io/usage/validators/

class Spend(BaseModel):
    points: int

# Response Body models ------------------------------------------------------------
class SpendResponse(BaseModel):
    payer: Payer
    points: int

class BalanceResponse(BaseModel):
    __root__: Dict[Payer, int]


# Endpoint functions -----------------------------------------------------------``
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

# router that handles all the operations on the user's points balance
@app.get("/users/{user_id}: str/{user_route}")
async def get_route(user_route: UserRoute, user_id: str):
    if user_route == UserRoute.add:
        return {"model_name": user_route, "user_id": user_id, "message": "going to add a transaction"}

    if user_route == UserRoute.spend:
        return {"model_name": user_route, "user_id": user_id, "message": "going to spend points"}

    if user_route == UserRoute.points:
        return {"model_name": user_route, "user_id": user_id, "message": "going to get points"}