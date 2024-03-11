from sqlalchemy.ext.asyncio import AsyncSession

from src.dao import DaoCurrencyRepository
from src.dto import ExchangeRateDTO
from src.model import ExchangeRate, Currency
from src.service import CurrencyService


class ExchangeRateService:

    @staticmethod
    async def get_exchange_rate_dto(session: AsyncSession, exchange_rate: ExchangeRate) -> ExchangeRateDTO:
        """
        Метод создает DTO объект на основе объекта модели класса ExchangeRate
        :param session: объект асинхронной сессии AsyncSession
        :param exchange_rate: объект класса ExchangeRate
        :return: объект класса ExchangeRateDTO
        """
        dao_currency_obj = DaoCurrencyRepository()
        currency_service_obj = CurrencyService()

        base_currency = await dao_currency_obj.find_by_id(
            session=session,
            currency_id=exchange_rate.base_currency_id
        )
        target_currency = await dao_currency_obj.find_by_id(
            session=session,
            currency_id=exchange_rate.target_currency_id
        )

        if isinstance(base_currency, Currency) and isinstance(target_currency, Currency):
            base_currency_dto = currency_service_obj.get_currency_dto(base_currency)
            target_currency_dto = currency_service_obj.get_currency_dto(target_currency)

            exchange_rate_obj = ExchangeRateDTO(
                exchange_rate_id=exchange_rate.id,
                base_currency=base_currency_dto,
                target_currency=target_currency_dto,
                rate=exchange_rate.rate,
            )

            return exchange_rate_obj
