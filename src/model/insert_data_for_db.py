import asyncio

from src.model.database import Base, db_helper
from src.model.models import Currencies


engine = db_helper.engine
session_factory = db_helper.session_factory


class CreateTablesDataBase:
    """
    Класс для создания таблиц, а также для их удаления, если это потребуется
    Таблицы создаются с помощью миграций, поэтому методы для создания и удаления не использовать
    Метод insert_data_currencies для заполнения таблицы currencies тестовыми данными
    Метод insert_data_exchangerates для заполнения таблицы exchangerates тестовыми данными
    """

    @staticmethod
    def drop_tables():
        """
        Метод удаляет все записи из БД и удаляет таблицы из базы данных currency_exchange
        :return: None
        """
        Base.metadata.drop_all(engine)

    @staticmethod
    def create_tables():
        """
        Метод создает две таблицы в базе данных currency_exchange:
        currencies - таблица с данными по всем валютам
        exchangerates - таблица с данными по обменным курсам
        :return: None
        """
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    async def insert_data_currencies(self):
        """
        Метод добавляет много валют в таблицу currencies
        Данные берутся из файла currencies.txt - это 43 валюты с сайта ЦБ РФ
        :return: None
        """
        currencies_dict = self.get_dict_currencies()
        if currencies_dict:
            currencies_list = [Currencies(code=code,
                                          full_name=full_name,
                                          sign='$') for code, full_name in currencies_dict.items()]
            async with session_factory() as session:
                session.add_all(currencies_list)
                await session.commit()

    @staticmethod
    def get_dict_currencies() -> dict:
        with open("static/currencies.txt", "r", encoding="UTF-8") as file:
            content = file.readlines()

        currencies_dict = {}

        for currency in content:
            key, value = currency.split('\t')
            value = value.strip()
            currencies_dict[key] = value

        return currencies_dict


data_base_obj = CreateTablesDataBase()

# asyncio.run(data_base_obj.create_tables()) # не требуется выполнять, т.к. создал таблицы с помощью миграции alembic
asyncio.run(data_base_obj.insert_data_currencies())
