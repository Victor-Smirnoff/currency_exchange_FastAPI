from fastapi import APIRouter, Depends, Query

from src.dao import DaoCurrencyRepository, DaoExchangeRepository, dao_currency_repository, dao_exchange_repository
from src.service import ExchangeService, exchange_service, CurrencyService, currency_service
from src.exception import ExchangerateException
from src.dto import ExchangeResponse


router = APIRouter(tags=["exchange"])


@router.get("/exchange")
async def get_exchange(
    currency_from: str = Query(..., alias="from"),
    currency_to: str = Query(..., alias="to"),
    amount: float = Query(...),
    exchange_service_obj: ExchangeService = Depends(exchange_service),
    dao_currency_obj: DaoCurrencyRepository = Depends(dao_currency_repository),
    dao_exchange_obj: DaoExchangeRepository = Depends(dao_exchange_repository),
    currency_service_obj: CurrencyService = Depends(currency_service),
):
    response = await exchange_service_obj.convert_currency(
        currency_from=currency_from,
        currency_to=currency_to,
        amount=amount,
        dao_currency_obj=dao_currency_obj,
        dao_exchange_obj=dao_exchange_obj
    )

    if isinstance(response, ExchangeResponse):
        exchange = await exchange_service_obj.get_exchange_dto(
            exchange_obj=response,
            currency_service_obj=currency_service_obj
        )
        return exchange
    else:
        raise ExchangerateException(
            message=response.message,
            status_code=response.code
        )
