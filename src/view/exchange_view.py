import decimal
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao import DaoExchangeRepository
from src.exception import ExchangerateException
from src.model import db_helper, ExchangeRate

router = APIRouter(tags=["exchange"])
dao_obj = DaoExchangeRepository()


@router.get("/exchange?from={base_currency_code}&to={target_currency_code}&amount=${amount}")
async def get_exchange(
        base_currency_code: Annotated[str, Path(max_length=3)],
        target_currency_code: Annotated[str, Path(max_length=3)],
        amount: int,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    pass
