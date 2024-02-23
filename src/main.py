import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.exception import CurrencyException, ExchangerateException
from src.view import currencies_router
from src.view import exchange_rates_router

app = FastAPI()
app.include_router(currencies_router)
app.include_router(exchange_rates_router)


@app.exception_handler(CurrencyException)
async def currency_exception_handler(request: Request, exc: CurrencyException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


@app.exception_handler(ExchangerateException)
async def exchange_rate_exception_handler(request: Request, exc: ExchangerateException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
