from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.model import Currencies


class DaoCurrencyRepository:
    """
    Класс для выполнения основных операций в БД над таблицей Currencies
    """

    @staticmethod
    async def find_all(session: AsyncSession) -> list[Currencies]:
        """
        Метод возвращает список объектов класса Currencies
        :param session: объект асинхронной сессии AsyncSession
        :return: list[Currencies]
        """
        stmt = select(Currencies).order_by(Currencies.id)
        result: Result = await session.execute(stmt)
        list_all_currencies = result.scalars().all()
        return list(list_all_currencies)
