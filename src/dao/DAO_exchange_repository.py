from sqlalchemy import select, Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.dto import ErrorResponse, ExchangeRateDTO
from src.model import ExchangeRate, Currency
from src.dao import DaoCurrencyRepository


class DaoExchangeRepository:
    """
    Класс для выполнения основных операций в БД над таблицей ExchangeRate
    """

    @staticmethod
    async def find_all(session: AsyncSession) -> list[ExchangeRate] | ErrorResponse:
        """
        Метод возвращает список объектов класса ExchangeRate или объект ошибки ErrorResponse
        :param session: объект асинхронной сессии AsyncSession
        :return: list[ExchangeRate] или ErrorResponse
        """
        try:
            stmt = select(ExchangeRate).order_by(ExchangeRate.id)
            result: Result = await session.execute(stmt)
            list_all_exchangerates = result.scalars().all()
            return list(list_all_exchangerates)
        except SQLAlchemyError:
            response = ErrorResponse(code=500, message=f"База данных недоступна")
            return response

    @staticmethod
    async def get_exchange_rate_dto(session: AsyncSession, exchange_rate: ExchangeRate) -> ExchangeRateDTO:
        """
        Метод создает DTO объект на основе объекта модели класса ExchangeRate
        :param session: объект асинхронной сессии AsyncSession
        :param exchange_rate: объект класса ExchangeRate
        :return: объект класса ExchangeRateDTO
        """
        dao_currency_obj = DaoCurrencyRepository()

        base_currency = await dao_currency_obj.find_by_id(
            session=session,
            currency_id=exchange_rate.base_currency_id
        )
        target_currency = await dao_currency_obj.find_by_id(
            session=session,
            currency_id=exchange_rate.target_currency_id
        )

        if isinstance(base_currency, Currency) and isinstance(target_currency, Currency):
            base_currency_dto = dao_currency_obj.get_currency_dto(base_currency)
            target_currency_dto = dao_currency_obj.get_currency_dto(target_currency)

            exchange_rate_obj = ExchangeRateDTO(
                id=exchange_rate.id,
                baseCurrency=base_currency_dto,
                targetCurrency=target_currency_dto,
                rate=exchange_rate.rate,
            )

            return exchange_rate_obj
