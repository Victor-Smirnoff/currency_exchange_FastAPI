from sqlalchemy import select, Result
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.dto import ErrorResponse, CurrencyDTO
from src.model import Currency


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
        except SQLAlchemyError:
            response = ErrorResponse(code=500, message=f"База данных недоступна")
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
        except SQLAlchemyError:
            response = ErrorResponse(code=500, message=f"База данных недоступна")
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
        except SQLAlchemyError:
            response = ErrorResponse(code=500, message=f"База данных недоступна")
            return response

    @staticmethod
    async def create_currency(
        session: AsyncSession,
        currency_name: str,
        currency_code: str,
        currency_sign: str,
    ) -> Currency | ErrorResponse:
        """
        Метод записывает новую валюту в БД
        :param session: объект асинхронной сессии AsyncSession
        :param currency_name: имя валюты
        :param currency_code: код валюты
        :param currency_sign: символ валюты
        :return: объект класса Currency | ErrorResponse
        """

        if not all((currency_name, currency_code, currency_sign)):
            response = ErrorResponse(code=400, message="Отсутствует нужное поле формы")
            return response

        try:
            new_currency = Currency(code=currency_code, full_name=currency_name, sign=currency_sign)
            session.add(new_currency)
            try:
                await session.commit()
                await session.refresh(new_currency)
                return new_currency
            except IntegrityError:
                response = ErrorResponse(code=409, message=f"Валюта с таким кодом “{currency_code}” уже существует")
                return response

        except SQLAlchemyError:
            response = ErrorResponse(code=500, message=f"База данных недоступна")
            return response

    async def delete_currency(self, session: AsyncSession, code: str) -> Currency | ErrorResponse:
        """
        Метод для удаления валюты из таблицы
        :param session: объект асинхронной сессии AsyncSession
        :param code: код валюты
        :return: объект класса Currency | ErrorResponse
        """
        if code == "":
            response = ErrorResponse(code=400, message="Код валюты отсутствует в адресе")
            return response

        currency = await self.find_by_code(session=session, code=code)
        if isinstance(currency, Currency):
            try:
                await session.delete(currency)
                await session.commit()
                return currency

            except SQLAlchemyError:
                response = ErrorResponse(code=500, message=f"База данных недоступна")
                return response
        else:
            return currency
