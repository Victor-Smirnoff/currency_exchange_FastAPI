from sqlalchemy import select, Result, and_
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

    @staticmethod
    async def find_by_id(session: AsyncSession, exchange_rate_id: int) -> ExchangeRate | ErrorResponse:
        """
        Метод возвращает найденный объект класса ExchangeRate если он найден в БД, иначе объект ErrorResponse
        :param session: объект асинхронной сессии AsyncSession
        :param exchange_rate_id: айди обменного курса
        :return: объект класса ExchangeRate или ErrorResponse
        """
        try:
            exchange_rate = await session.get(ExchangeRate, exchange_rate_id)
            if isinstance(exchange_rate, ExchangeRate):
                return exchange_rate
            else:
                response = ErrorResponse(code=404, message=f"Обменный курс с id {exchange_rate_id} не найден")
                return response
        except SQLAlchemyError:
            response = ErrorResponse(code=500, message=f"База данных недоступна")
            return response

    @staticmethod
    async def find_by_codes(session: AsyncSession, currency_codes: str) -> ExchangeRate | ErrorResponse:
        """
        Метод возвращает найденный объект класса ExchangeRate если он найден в БД, иначе объект ErrorResponse
        :param session: объект асинхронной сессии AsyncSession
        :param currency_codes: коды валют в адресе запроса
        :return: объект класса ExchangeRate или ErrorResponse
        """
        if not currency_codes or len(currency_codes) != 6:
            response = ErrorResponse(
                code=400,
                message="Коды валют отсутствуют в адресе или длина двух кодов валют не равна 6"
            )
            return response

        base_currency_code = currency_codes[:3]
        target_currency_code = currency_codes[3:]

        try:
            stmt = (select(ExchangeRate).where(and_(
                    ExchangeRate.base_currency_id == select(Currency.id).where(
                        Currency.code == base_currency_code),
                    ExchangeRate.target_currency_id == select(Currency.id).where(
                        Currency.code == target_currency_code))
            ))

            result: Result = await session.execute(stmt)
            if isinstance(result, Result):
                exchange_rate = result.scalar()
                if isinstance(exchange_rate, ExchangeRate):
                    return exchange_rate
                else:
                    if currency_codes == "":
                        response = ErrorResponse(code=400, message="Коды валют пары отсутствуют в адресе")
                    else:
                        response = ErrorResponse(
                            code=404,
                            message=f"Обменный курс для пары “{currency_codes}” не найден"
                        )
                    return response

        except SQLAlchemyError:
            response = ErrorResponse(code=500, message=f"База данных недоступна")
            return response
