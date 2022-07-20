import datetime
from typing import Dict, List
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
# Payers are partner companies that can supply points for users (in exchange for loyalty to their products)
# Payers must be registered with the system beforehand and only registered partners can supply points via tranasaction payloads
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


# Represents a spend request for a user
class Spend(BaseModel):
    points: int

# Response Body models ------------------------------------------------------------
class Spender(BaseModel):
    payer: Payer
    points: int

class SpendReponse(BaseModel):
    spenders: List[Spender]

class BalanceResponse(BaseModel):
    # __root__ is our way to tell Pydantic that our model doesn’t represent a regular key-value model.
    __root__: Dict[Payer, int]


# Internal Data Models ---------------------------------------------------------
# TODO find way to store a persistent representation of data in web server
# considering: local storage to start, then DB using SQLAlchemy - see https://fastapi.tiangolo.com/tutorial/sql-databases/
# User class
class User(BaseModel):
    id: int # path variable used to get user resource
    name: str
    email: str
    points: int # determined by transactions
    created_at: datetime.datetime
    updated_at: datetime.datetime
    transactions: Dict[Transaction] #stores all transactions for a user 
    expenditures: Dict[Spend] #stores all expenditures for a user -> affects the balance response
    balanceResponse: BalanceResponse #stores the points balance for each payer (partner firm)

# Users class - set of users
class Users(BaseModel):
    __root__: Dict[int, User]

# TODO figure out if it is redundant to store a model equivalent to the balance response in the user class
# class UserPayers(BaseModel):
#     __root__: Dict[Payer, int]

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

# get the points balance for a user -> return balance response
@app.get("/users/{user_id}: str/{user_route}")
async def get_route(user_route: UserRoute, user_id: str):
    if user_route == UserRoute.points:
        return {"model_name": user_route, "user_id": user_id, "message": "going to get points"}

# spend points for a user -> return spend response  
@app.put("/users/{user_id}/{user_route}")
async def put_route(user_route: UserRoute, user_id: str):
    if user_route == UserRoute.spend:
        return {"model_name": user_route, "user_id": user_id, "message": "going to spend points"}

# add transactions for a specific Payer and date
@app.post("/users/{user_id}/{user_route}")
async def post_route(user_route: UserRoute, user_id: str):
    if user_route == UserRoute.add:
        return {"model_name": user_route, "user_id": user_id, "message": "going to add a transaction"}