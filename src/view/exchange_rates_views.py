from fastapi import APIRouter


router = APIRouter(tags=["exchange_rates"])


@router.get("/exchangeRates")
async def exchange_rates():
    return ["list all exchange_rates"]
