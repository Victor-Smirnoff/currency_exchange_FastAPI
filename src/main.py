import uvicorn
from fastapi import FastAPI, Form

from typing import Annotated


app = FastAPI()


@app.get("/")
async def index():
    return {"message": "главная страница"}


@app.get("/currencies")
async def currencies():
    return ["list all currencies"]


@app.post("/currencies")
async def currencies(name: Annotated[str, Form()], code: Annotated[str, Form()], sign: Annotated[str, Form()]):
    return {"name": name, "code": code, "sign": sign}


@app.get("/currency/{code}")
async def currency(code):
    return {"currency": code}


@app.get("/exchangeRates")
async def exchange_rates():
    return ["list all exchange_rates"]


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
