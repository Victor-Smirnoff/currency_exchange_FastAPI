from typing import Annotated, Union
from fastapi import APIRouter, Form, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao import DaoCurrencyRepository
from src.dto_response import ErrorResponse
from src.model import Currencies, db_helper


router = APIRouter(tags=["currencies"])
dao_obj_currencies = DaoCurrencyRepository()


@router.get("/currencies")
async def get_all_currencies(
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    await dao_obj_currencies.find_all(session)


# @router.post("/currencies")
# async def currencies(
#     name: Annotated[str, Form(..., min_length=3, max_length=30)],
#     code: Annotated[str, Form(..., min_length=3, max_length=3)],
#     sign: Annotated[str, Form(..., min_length=1, max_length=5)],
# ):
#     return {"name": name, "code": code, "sign": sign}
#
#
# @router.get("/currency/{code}", response_model=Currencies)
# async def currency(code: Annotated[str, Path(min_length=3, max_length=3)]):
#     return {"currency": code}
