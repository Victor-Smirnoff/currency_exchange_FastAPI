from typing import Annotated, Optional
from fastapi import APIRouter, Form, Path, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao import DaoCurrencyRepository
from src.exception import CurrencyException
from src.model import db_helper
from src.model import Currency


router = APIRouter(tags=["currencies"])
dao_obj = DaoCurrencyRepository()


@router.get("/currencies")
async def get_all_currencies(
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    all_currencies_list = await dao_obj.find_all(session)
    if isinstance(all_currencies_list, list):
        response = [dao_obj.get_currency_dto(currency) for currency in all_currencies_list]
        return response
    else:
        response = all_currencies_list
        raise HTTPException(
            status_code=response.code,
            detail={"message": response.message}
        )


@router.get("/currency")
async def get_currency_by_empty_code(
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    response = await dao_obj.find_by_code(session=session, code="")

    raise CurrencyException(
        message=response.message,
        status_code=response.code
    )


@router.get("/currency/{code}")
async def get_currency_by_code(
        code: Annotated[str, Path(max_length=3)],
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    response = await dao_obj.find_by_code(session=session, code=code)
    if isinstance(response, Currency):
        currency = dao_obj.get_currency_dto(response)
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
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    response = await dao_obj.create_currency(
        session=session,
        currency_name=name,
        currency_code=code,
        currency_sign=sign,
    )
    if isinstance(response, Currency):
        currency = dao_obj.get_currency_dto(response)
        return currency
    else:
        raise CurrencyException(
            message=response.message,
            status_code=response.code
        )


@router.delete("/currencies", status_code=200)
async def delete_currency(
    code: Annotated[Optional[str], Form(max_length=3)] = "",
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    response = await dao_obj.delete_currency(session=session, code=code)
    if isinstance(response, Currency):
        currency = dao_obj.get_currency_dto(response)
        return currency
    else:
        raise CurrencyException(
            message=response.message,
            status_code=response.code
        )
