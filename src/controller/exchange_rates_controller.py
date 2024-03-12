import decimal
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Form

from src.dao import DaoExchangeRepository, dao_exchange_repository, DaoCurrencyRepository, dao_currency_repository
from src.exception import ExchangerateException
from src.model import ExchangeRate
from src.service import exchange_rate_service, ExchangeRateService, CurrencyService, currency_service

router = APIRouter(tags=["exchange_rates"])


@router.get("/exchangeRates")
async def get_all_exchange_rates(
    dao_exchange_obj: DaoExchangeRepository = Depends(dao_exchange_repository),
    exchange_rate_service_obj: ExchangeRateService = Depends(exchange_rate_service),
    dao_currency_obj: DaoCurrencyRepository = Depends(dao_currency_repository),
    currency_service_obj: CurrencyService = Depends(currency_service),
):
    all_exchangerates_list = await dao_exchange_obj.find_all()
    if isinstance(all_exchangerates_list, list):
        response = [await exchange_rate_service_obj.get_exchange_rate_dto(
            exchange_rate=exchange_rate,
            currency_service_obj=currency_service_obj,
            dao_currency_obj=dao_currency_obj,
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
    dao_exchange_obj: DaoExchangeRepository = Depends(dao_exchange_repository),
):
    response = await dao_exchange_obj.find_by_codes(base_currency_code="", target_currency_code="")

    raise ExchangerateException(
        message=response.message,
        status_code=response.code
    )


@router.get("/exchangeRate/{currency_codes}")
async def get_exchange_rates_by_currency_codes(
    currency_codes: Annotated[str, Path(max_length=6)],
    dao_exchange_obj: DaoExchangeRepository = Depends(dao_exchange_repository),
    exchange_rate_service_obj: ExchangeRateService = Depends(exchange_rate_service),
    dao_currency_obj: DaoCurrencyRepository = Depends(dao_currency_repository),
    currency_service_obj: CurrencyService = Depends(currency_service),
):
    base_currency_code = currency_codes[:3]
    target_currency_code = currency_codes[3:]
    response = await dao_exchange_obj.find_by_codes(
        base_currency_code=base_currency_code,
        target_currency_code=target_currency_code
    )
    if isinstance(response, ExchangeRate):
        exchange_rate = await exchange_rate_service_obj.get_exchange_rate_dto(
            exchange_rate=response,
            currency_service_obj=currency_service_obj,
            dao_currency_obj=dao_currency_obj,
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
    dao_exchange_obj: DaoExchangeRepository = Depends(dao_exchange_repository),
    exchange_rate_service_obj: ExchangeRateService = Depends(exchange_rate_service),
    dao_currency_obj: DaoCurrencyRepository = Depends(dao_currency_repository),
    currency_service_obj: CurrencyService = Depends(currency_service),
):
    response = await dao_exchange_obj.create_exchange_rate(
        base_currency_code=baseCurrencyCode,
        target_currency_code=targetCurrencyCode,
        rate=rate,
        dao_currency_obj=dao_currency_obj,
    )
    if isinstance(response, ExchangeRate):
        exchange_rate = await exchange_rate_service_obj.get_exchange_rate_dto(
            exchange_rate=response,
            currency_service_obj=currency_service_obj,
            dao_currency_obj=dao_currency_obj,
        )
        return exchange_rate
    else:
        raise ExchangerateException(
            message=response.message,
            status_code=response.code
        )


@router.patch("/exchangeRate/{currency_codes}")
async def get_exchange_rates_by_currency_codes(
    currency_codes: Annotated[str, Path(max_length=6)],
    rate: Annotated[Optional[decimal.Decimal], Form()] = "",
    dao_exchange_obj: DaoExchangeRepository = Depends(dao_exchange_repository),
    exchange_rate_service_obj: ExchangeRateService = Depends(exchange_rate_service),
    dao_currency_obj: DaoCurrencyRepository = Depends(dao_currency_repository),
    currency_service_obj: CurrencyService = Depends(currency_service),
):
    base_currency_code = currency_codes[:3]
    target_currency_code = currency_codes[3:]

    response = await dao_exchange_obj.update_exchange_rate(
        base_currency_code=base_currency_code,
        target_currency_code=target_currency_code,
        rate=rate,
    )

    if isinstance(response, ExchangeRate):
        exchange_rate = await exchange_rate_service_obj.get_exchange_rate_dto(
            exchange_rate=response,
            currency_service_obj=currency_service_obj,
            dao_currency_obj=dao_currency_obj,
        )
        return exchange_rate
    else:
        raise ExchangerateException(
            message=response.message,
            status_code=response.code
        )


@router.delete("/exchangeRate/{currency_codes}")
async def get_exchange_rates_by_currency_codes(
    currency_codes: Annotated[str, Path(max_length=6)],
    dao_exchange_obj: DaoExchangeRepository = Depends(dao_exchange_repository),
    exchange_rate_service_obj: ExchangeRateService = Depends(exchange_rate_service),
    dao_currency_obj: DaoCurrencyRepository = Depends(dao_currency_repository),
    currency_service_obj: CurrencyService = Depends(currency_service),
):
    base_currency_code = currency_codes[:3]
    target_currency_code = currency_codes[3:]

    response = await dao_exchange_obj.delete_exchange_rate(
        base_currency_code=base_currency_code,
        target_currency_code=target_currency_code,
    )

    if isinstance(response, ExchangeRate):
        exchange_rate = await exchange_rate_service_obj.get_exchange_rate_dto(
            exchange_rate=response,
            currency_service_obj=currency_service_obj,
            dao_currency_obj=dao_currency_obj,
        )
        return exchange_rate
    else:
        raise ExchangerateException(
            message=response.message,
            status_code=response.code
        )
