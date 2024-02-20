from sqlalchemy import select, Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union
from src.dto_response import ErrorResponse
from src.model import Currencies


class DaoCurrencyRepository:
    """
    Класс для выполнения основных операций в БД над таблицей Currencies
    """

    @staticmethod
    async def find_all(session: AsyncSession) -> Union[list[Currencies], ErrorResponse]:
        """
        Метод возвращает список объектов класса Currencies
        :param session: объект асинхронной сессии AsyncSession
        :return: list[Currencies]
        """
        try:
            stmt = select(Currencies).order_by(Currencies.id)
            result: Result = await session.execute(stmt)
            list_all_currencies = result.scalars().all()
            return list(list_all_currencies)
        except SQLAlchemyError as e:
            response = ErrorResponse(code=500, message=f"База данных недоступна: {e}")
            return response

    @staticmethod
    async def find_by_id(session: AsyncSession, currency_id: int) -> Union[Currencies, ErrorResponse]:
        """
        Метод возвращает найденный объект класса Currencies если он найден в БД, иначе объект ErrorResponse
        :param session: объект асинхронной сессии AsyncSession
        :param currency_id: айди валюты
        :return: объект класса Currencies или ErrorResponse
        """
        try:
            stmt = select(Currencies).where(Currencies.id == currency_id)
            result: Result = await session.execute(stmt)
            currency = result.scalars().one()
            if isinstance(currency, Currencies):
                return currency
            else:
                response = ErrorResponse(code=404, message=f"Валюта с id {currency_id} не найдена")
                return response
        except SQLAlchemyError as e:
            response = ErrorResponse(code=500, message=f"База данных недоступна: {e}")
            return response
