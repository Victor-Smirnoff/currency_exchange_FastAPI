from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.service import ExchangeService
from src.exception import ExchangerateException
from src.model import db_helper
from src.dto import ExchangeResponse


router = APIRouter(tags=["exchange"])
dao_obj = ExchangeService()


@router.get("/exchange")
async def get_exchange(
        currency_from: str = Query(..., alias="from"),
        currency_to: str = Query(..., alias="to"),
        amount: float = Query(...),
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    response = await dao_obj.convert_currency(
        session=session,
        currency_from=currency_from,
        currency_to=currency_to,
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
