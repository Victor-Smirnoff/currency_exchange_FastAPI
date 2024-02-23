from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao import DaoExchangeRepository
from src.model import db_helper

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
