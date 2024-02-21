import asyncio

from sqlalchemy import select, Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from src.dto_response import ErrorResponse
from src.model import Currencies


class DaoCurrencyRepository:
    """
    Класс для выполнения основных операций в БД над таблицей Currencies
    """

    @staticmethod
    async def find_all(session: AsyncSession) -> list[Currencies] | ErrorResponse:
        """
        Метод возвращает список объектов класса Currencies или объект ошибки ErrorResponse
        :param session: объект асинхронной сессии AsyncSession
        :return: list[Currencies] или ErrorResponse
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
    async def find_by_id(session: AsyncSession, currency_id: int) -> Currencies | ErrorResponse:
        """
        Метод возвращает найденный объект класса Currencies если он найден в БД, иначе объект ErrorResponse
        :param session: объект асинхронной сессии AsyncSession
        :param currency_id: айди валюты
        :return: объект класса Currencies или ErrorResponse
        """
        try:
            currency = await session.get(Currencies, currency_id)
            if isinstance(currency, Currencies):
                return currency
            else:
                response = ErrorResponse(code=404, message=f"Валюта с id {currency_id} не найдена")
                return response
        except SQLAlchemyError as e:
            response = ErrorResponse(code=500, message=f"База данных недоступна: {e}")
            return response

    @staticmethod
    async def find_by_code(session: AsyncSession, code: str) -> Currencies | ErrorResponse:
        """
        Метод возвращает найденный объект класса Currencies если он найден в БД, иначе объект ErrorResponse
        :param session: объект асинхронной сессии AsyncSession
        :param code: код валюты
        :return: объект класса Currencies или ErrorResponse
        """
        try:
            stmt = select(Currencies).where(Currencies.code == code)
            result: Result = await session.execute(stmt)
            if isinstance(result, Result):
                currency = result.scalar()
                if isinstance(currency, Currencies):
                    return currency
                else:
                    if code == "":
                        response = ErrorResponse(code=400, message="Код валюты отсутствует в адресе")
                    else:
                        response = ErrorResponse(code=404, message=f"Валюта “{code}” не найдена")
                    return response
        except SQLAlchemyError as e:
            response = ErrorResponse(code=500, message=f"База данных недоступна: {e}")
            return response

    @staticmethod
    def get_correct_currency_dict(currency: Currencies) -> dict:
        """
        Метод делает правильный словарь для отправки в REST API
        :param currency: объект класса Currencies
        :return: dict формата {"id": id, "name": name, "code": code, "sign": sign}
        """
        currency_dict = {
            "id": currency.id,
            "name": currency.full_name,
            "code": currency.code,
            "sign": currency.sign,
        }

        return currency_dict
