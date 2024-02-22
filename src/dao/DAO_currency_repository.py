from sqlalchemy import select, Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from src.dto_response import ErrorResponse
from src.model import Currency
from src.schema import CurrencyCreate


class DaoCurrencyRepository:
    """
    Класс для выполнения основных операций в БД над таблицей Currency
    """

    @staticmethod
    async def find_all(session: AsyncSession) -> list[Currency] | ErrorResponse:
        """
        Метод возвращает список объектов класса Currency или объект ошибки ErrorResponse
        :param session: объект асинхронной сессии AsyncSession
        :return: list[Currency] или ErrorResponse
        """
        try:
            stmt = select(Currency).order_by(Currency.id)
            result: Result = await session.execute(stmt)
            list_all_currencies = result.scalars().all()
            return list(list_all_currencies)
        except SQLAlchemyError as e:
            response = ErrorResponse(code=500, message=f"База данных недоступна: {e}")
            return response

    @staticmethod
    async def find_by_id(session: AsyncSession, currency_id: int) -> Currency | ErrorResponse:
        """
        Метод возвращает найденный объект класса Currency если он найден в БД, иначе объект ErrorResponse
        :param session: объект асинхронной сессии AsyncSession
        :param currency_id: айди валюты
        :return: объект класса Currency или ErrorResponse
        """
        try:
            currency = await session.get(Currency, currency_id)
            if isinstance(currency, Currency):
                return currency
            else:
                response = ErrorResponse(code=404, message=f"Валюта с id {currency_id} не найдена")
                return response
        except SQLAlchemyError as e:
            response = ErrorResponse(code=500, message=f"База данных недоступна: {e}")
            return response

    @staticmethod
    async def find_by_code(session: AsyncSession, code: str) -> Currency | ErrorResponse:
        """
        Метод возвращает найденный объект класса Currency если он найден в БД, иначе объект ErrorResponse
        :param session: объект асинхронной сессии AsyncSession
        :param code: код валюты
        :return: объект класса Currency или ErrorResponse
        """
        try:
            stmt = select(Currency).where(Currency.code == code)
            result: Result = await session.execute(stmt)
            if isinstance(result, Result):
                currency = result.scalar()
                if isinstance(currency, Currency):
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
    def get_correct_currency_dict(currency: Currency) -> dict:
        """
        Метод делает правильный словарь для отправки в REST API
        :param currency: объект класса Currency
        :return: dict формата {"id": id, "name": name, "code": code, "sign": sign}
        """
        currency_dict = {
            "id": currency.id,
            "name": currency.full_name,
            "code": currency.code,
            "sign": currency.sign,
        }

        return currency_dict

    @staticmethod
    async def create_currency(session: AsyncSession, new_currency: CurrencyCreate) -> Currency:
        currency = Currency(**new_currency.model_dump())
        session.add(currency)
        await session.commit()
        await session.refresh(currency)
        return currency
