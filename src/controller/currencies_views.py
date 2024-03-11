from typing import Annotated, Optional
from fastapi import APIRouter, Form, Path, Depends, HTTPException

from src.dao import DaoCurrencyRepository, dao_currency_repository
from src.exception import CurrencyException
from src.model import Currency
from src.service import CurrencyService, currency_service


router = APIRouter(tags=["currencies"])


@router.get("/currencies")
async def get_all_currencies(
    dao_currency_obj: DaoCurrencyRepository = Depends(dao_currency_repository),
    currency_service_obj: CurrencyService = Depends(currency_service),
):
    all_currencies_list = await dao_currency_obj.find_all()
    if isinstance(all_currencies_list, list):
        response = [currency_service_obj.get_currency_dto(currency) for currency in all_currencies_list]
        return response
    else:
        response = all_currencies_list
        raise HTTPException(
            status_code=response.code,
            detail={"message": response.message}
        )


@router.get("/currency")
async def get_currency_by_empty_code(
    dao_currency_obj: DaoCurrencyRepository = Depends(dao_currency_repository),
):
    response = await dao_currency_obj.find_by_code(code="")

    raise CurrencyException(
        message=response.message,
        status_code=response.code
    )


@router.get("/currency/{code}")
async def get_currency_by_code(
    code: Annotated[str, Path(max_length=3)],
    dao_currency_obj: DaoCurrencyRepository = Depends(dao_currency_repository),
    currency_service_obj: CurrencyService = Depends(currency_service),
):
    response = await dao_currency_obj.find_by_code(code=code)
    if isinstance(response, Currency):
        currency = currency_service_obj.get_currency_dto(response)
        return currency
    else:
        raise CurrencyException(
            message=response.message,
            status_code=response.code
        )


@router.post("/currencies", status_code=201)
async def create_currency(
    name: Annotated[Optional[str], Form(max_length=30)] = "",
    code: Annotated[Optional[str], Form(max_length=3)] = "",
    sign: Annotated[Optional[str], Form(max_length=5)] = "",
    dao_currency_obj: DaoCurrencyRepository = Depends(dao_currency_repository),
    currency_service_obj: CurrencyService = Depends(currency_service),
):
    response = await dao_currency_obj.create_currency(
        currency_name=name,
        currency_code=code,
        currency_sign=sign,
    )
    if isinstance(response, Currency):
        currency = currency_service_obj.get_currency_dto(response)
        return currency
    else:
        raise CurrencyException(
            message=response.message,
            status_code=response.code
        )


@router.delete("/currencies", status_code=200)
async def delete_currency(
    code: Annotated[Optional[str], Form(max_length=3)] = "",
    dao_currency_obj: DaoCurrencyRepository = Depends(dao_currency_repository),
    currency_service_obj: CurrencyService = Depends(currency_service),
):
    response = await dao_currency_obj.delete_currency(code=code)
    if isinstance(response, Currency):
        currency = currency_service_obj.get_currency_dto(response)
        return currency
    else:
        raise CurrencyException(
            message=response.message,
            status_code=response.code
        )
