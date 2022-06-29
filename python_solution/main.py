import datetime
from typing import Dict
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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

class BalanceResponse(BaseModel):
    __root__: Dict[Payer, int]



@app.get("/status")
async def status():
    return {"status": "web server working"}

    

@app.post("/transactions/")
async def create_transaction(transaction: Transaction):
    return transaction
