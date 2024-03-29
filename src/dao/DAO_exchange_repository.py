import decimal

from fastapi import Depends
from sqlalchemy import select, Result, and_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.dto import ErrorResponse
from src.model import ExchangeRate, Currency, db_helper
from src.dao.DAO_currency_repository import DaoCurrencyRepository


class DaoExchangeRepository:
    """
    Класс для выполнения основных операций в БД над таблицей ExchangeRate
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_all(self) -> list[ExchangeRate] | ErrorResponse:
        """
        Метод возвращает список объектов класса ExchangeRate или объект ошибки ErrorResponse
        :return: list[ExchangeRate] или ErrorResponse
        """
        try:
            stmt = select(ExchangeRate).order_by(ExchangeRate.id)
            result: Result = await self.session.execute(stmt)
            list_all_exchangerates = result.scalars().all()
            return list(list_all_exchangerates)
        except SQLAlchemyError:
            response = ErrorResponse(code=500, message=f"База данных недоступна")
            return response

    async def find_by_id(self, exchange_rate_id: int) -> ExchangeRate | ErrorResponse:
        """
        Метод возвращает найденный объект класса ExchangeRate если он найден в БД, иначе объект ErrorResponse
        :param exchange_rate_id: айди обменного курса
        :return: объект класса ExchangeRate или ErrorResponse
        """
        try:
            exchange_rate = await self.session.get(ExchangeRate, exchange_rate_id)
            if isinstance(exchange_rate, ExchangeRate):
                return exchange_rate
            else:
                response = ErrorResponse(code=404, message=f"Обменный курс с id {exchange_rate_id} не найден")
                return response
        except SQLAlchemyError:
            response = ErrorResponse(code=500, message=f"База данных недоступна")
            return response

    async def find_by_codes(
        self,
        base_currency_code: str,
        target_currency_code: str,
    ) -> ExchangeRate | ErrorResponse:
        """
        Метод возвращает найденный объект класса ExchangeRate если он найден в БД, иначе объект ErrorResponse
        :param base_currency_code: код базовой валюты в адресе запроса
        :param target_currency_code: код целевой валюты в адресе запроса
        :return: объект класса ExchangeRate или ErrorResponse
        """

        if (not base_currency_code or not target_currency_code
                or len(base_currency_code) + len(target_currency_code) != 6):
            response = ErrorResponse(
                code=400,
                message="Коды валют отсутствуют в адресе или длина двух кодов валют не равна 6"
            )
            return response

        try:
            stmt = (select(ExchangeRate).where(and_(
                    ExchangeRate.base_currency_id == select(Currency.id).where(
                        Currency.code == base_currency_code),
                    ExchangeRate.target_currency_id == select(Currency.id).where(
                        Currency.code == target_currency_code))
            ))

            result: Result = await self.session.execute(stmt)
            if isinstance(result, Result):
                exchange_rate = result.scalar()
                if isinstance(exchange_rate, ExchangeRate):
                    return exchange_rate
                else:
                    if base_currency_code == "" or target_currency_code == "":
                        response = ErrorResponse(code=400, message="Коды валют пары отсутствуют в адресе")
                    else:
                        response = ErrorResponse(
                            code=404,
                            message=f"Обменный курс для пары “{base_currency_code}{target_currency_code}” не найден"
                        )
                    return response

        except SQLAlchemyError:
            response = ErrorResponse(code=500, message=f"База данных недоступна")
            return response

    async def create_exchange_rate(
        self,
        base_currency_code: str,
        target_currency_code: str,
        rate: decimal.Decimal,
        dao_currency_obj: DaoCurrencyRepository,
    ) -> ExchangeRate | ErrorResponse:
        """
        Метод для добавления нового обменного курса
        :param base_currency_code: код базовой валюты
        :param target_currency_code: код целевой валюты
        :param rate: обменный курс
        :param dao_currency_obj: здесь передается зависимость на объект класса DaoCurrencyRepository
        :return: объект класса ExchangeRate | ErrorResponse
        """

        if not all((base_currency_code, target_currency_code, rate)):
            response = ErrorResponse(code=400, message="Отсутствует нужное поле формы")
            return response

        try:
            base_currency = await dao_currency_obj.find_by_code(
                code=base_currency_code
            )
            target_currency = await dao_currency_obj.find_by_code(
                code=target_currency_code
            )

            if isinstance(base_currency, Currency) and isinstance(target_currency, Currency):
                base_currency_id = base_currency.id
                target_currency_id = target_currency.id

                new_exchange_rate = ExchangeRate(
                    base_currency_id=base_currency_id,
                    target_currency_id=target_currency_id,
                    rate=rate
                    )
                self.session.add(new_exchange_rate)
                try:
                    await self.session.commit()
                    await self.session.refresh(new_exchange_rate)
                    return new_exchange_rate
                except IntegrityError:
                    response = ErrorResponse(
                        code=409,
                        message=f"Валютная пара с таким кодом "
                                f"“{base_currency_code}{target_currency_code}” уже существует"
                    )
                    return response
            else:
                response = ErrorResponse(
                    code=404,
                    message=f"Одна (или обе) валюта из валютной пары “{base_currency_code}{target_currency_code}” "
                            f"не существует в БД"
                )
                return response

        except SQLAlchemyError:
            response = ErrorResponse(code=500, message=f"База данных недоступна")
            return response

    async def update_exchange_rate(
        self,
        base_currency_code: str,
        target_currency_code: str,
        rate: decimal.Decimal,
    ) -> ExchangeRate | ErrorResponse:
        """
        Метод для изменения существующего обменного курса
        :param base_currency_code: код базовой валюты
        :param target_currency_code: код целевой валюты
        :param rate: обменный курс
        :return: объект класса ExchangeRate | ErrorResponse
        """
        if isinstance(rate, str) and rate == "":
            response = ErrorResponse(code=400, message="Отсутствует нужное поле формы")
            return response

        try:
            exchange_rate = await self.find_by_codes(
                base_currency_code=base_currency_code,
                target_currency_code=target_currency_code,
            )
            if isinstance(exchange_rate, ExchangeRate):
                exchange_rate.rate = rate
                self.session.add(exchange_rate)
                await self.session.commit()
                return exchange_rate
            else:
                return exchange_rate
        except SQLAlchemyError:
            response = ErrorResponse(code=500, message=f"База данных недоступна")
            return response

    async def delete_exchange_rate(
        self,
        base_currency_code: str,
        target_currency_code: str,
    ) -> ExchangeRate | ErrorResponse:
        """
        Метод для удаления существующего обменного курса
        :param base_currency_code: код базовой валюты
        :param target_currency_code: код целевой валюты
        :return: объект класса ExchangeRate | ErrorResponse
        """

        try:
            exchange_rate = await self.find_by_codes(
                base_currency_code=base_currency_code,
                target_currency_code=target_currency_code,
            )
            if isinstance(exchange_rate, ExchangeRate):
                await self.session.delete(exchange_rate)
                await self.session.commit()
                return exchange_rate
            else:
                return exchange_rate
        except SQLAlchemyError:
            response = ErrorResponse(code=500, message=f"База данных недоступна")
            return response


async def dao_exchange_repository(session: AsyncSession = Depends(db_helper.session_dependency)):
    return DaoExchangeRepository(session=session)
