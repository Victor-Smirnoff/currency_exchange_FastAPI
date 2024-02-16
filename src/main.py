import uvicorn
from fastapi import FastAPI

from src.currencies_views import router as currencies_router
from src.exchange_rates_views import router as exchange_rates_router


app = FastAPI()
app.include_router(currencies_router)
app.include_router(exchange_rates_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
