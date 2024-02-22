from typing import Annotated
from fastapi import APIRouter, Form, Path, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao import DaoCurrencyRepository
from src.dto import CurrencyDTO
from src.exception import CurrencyException
from src.model import db_helper
from src.model import Currency
from src.schema import CurrencyCreate

router = APIRouter(tags=["currencies"])
dao_obj_currencies = DaoCurrencyRepository()


@router.get("/currencies")
async def get_all_currencies(
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    all_currencies_list = await dao_obj_currencies.find_all(session)
    if isinstance(all_currencies_list, list):
        response = [dao_obj_currencies.get_currency_dto(currency) for currency in all_currencies_list]
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
    response = await dao_obj_currencies.find_by_code(session=session, code="")

    raise CurrencyException(
        message=response.message,
        status_code=response.code
    )


@router.get("/currency/{code}")
async def get_currency_by_code(
        code: Annotated[str, Path(max_length=3)],
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    response = await dao_obj_currencies.find_by_code(session=session, code=code)
    if isinstance(response, Currency):
        currency = dao_obj_currencies.get_currency_dto(response)
        return currency
    else:
        raise CurrencyException(
            message=response.message,
            status_code=response.code
        )


@router.post("/currencies")
async def currencies(
    name: Annotated[str, Form(..., min_length=3, max_length=30)],
    code: Annotated[str, Form(..., min_length=3, max_length=3)],
    sign: Annotated[str, Form(..., min_length=1, max_length=5)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    new_currency = CurrencyCreate(full_name=name, code=code, sign=sign)
    return await dao_obj_currencies.create_currency(session=session, new_currency=new_currency)
