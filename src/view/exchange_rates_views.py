import decimal
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Form
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao import DaoExchangeRepository
from src.exception import ExchangerateException
from src.model import db_helper, ExchangeRate

router = APIRouter(tags=["exchange_rates"])
dao_obj = DaoExchangeRepository()


@router.get("/exchangeRates")
async def get_all_exchange_rates(
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    all_exchangerates_list = await dao_obj.find_all(session)
    if isinstance(all_exchangerates_list, list):
        response = [await dao_obj.get_exchange_rate_dto(
            session=session,
            exchange_rate=exchange_rate
        ) for exchange_rate in all_exchangerates_list
        ]
        return response
    else:
        response = all_exchangerates_list
        raise HTTPException(
            status_code=response.code,
            detail={"message": response.message}
        )


@router.get("/exchangeRate")
async def get_exchange_rates_by_empty_code(
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    response = await dao_obj.find_by_codes(session=session, currency_codes="")

    raise ExchangerateException(
        message=response.message,
        status_code=response.code
    )


@router.get("/exchangeRate/{currency_codes}")
async def get_exchange_rates_by_currency_codes(
        currency_codes: Annotated[str, Path(max_length=6)],
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    response = await dao_obj.find_by_codes(session=session, currency_codes=currency_codes)
    if isinstance(response, ExchangeRate):
        exchange_rate = await dao_obj.get_exchange_rate_dto(
            session=session,
            exchange_rate=response,
        )
        return exchange_rate
    else:
        raise ExchangerateException(
            message=response.message,
            status_code=response.code
        )


@router.post("/exchangeRates", status_code=201)
async def create_exchange_rate(
    baseCurrencyCode: Annotated[Optional[str], Form(max_length=3)] = "",
    targetCurrencyCode: Annotated[Optional[str], Form(max_length=3)] = "",
    rate: Annotated[Optional[decimal.Decimal], Form()] = "",
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    response = await dao_obj.create_exchange_rate(
        session=session,
        base_currency_code=baseCurrencyCode,
        target_currency_code=targetCurrencyCode,
        rate=rate,
    )
    if isinstance(response, ExchangeRate):
        exchange_rate = await dao_obj.get_exchange_rate_dto(session=session, exchange_rate=response)
        return exchange_rate
    else:
        raise ExchangerateException(
            message=response.message,
            status_code=response.code
        )
