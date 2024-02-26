import decimal
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.service import ExchangeService
from src.exception import ExchangerateException
from src.model import db_helper, ExchangeRate
from src.dto import ExchangeResponse, ErrorResponse


router = APIRouter(tags=["exchange"])
dao_obj = ExchangeService()


@router.get("/exchange?from={base_currency_code}&to={target_currency_code}&amount=${amount}")
async def get_exchange(
        base_currency_code: Annotated[str, Path(max_length=3)],
        target_currency_code: Annotated[str, Path(max_length=3)],
        amount: float,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    response = await dao_obj.convert_currency(
        session=session,
        currency_from=base_currency_code,
        currency_to=target_currency_code,
        amount=amount,
    )

    if isinstance(response, ExchangeResponse):
        exchange = await dao_obj.get_exchange_dto(exchange_obj=response)
        return exchange
    else:
        raise ExchangerateException(
            message=response.message,
            status_code=response.code
        )
