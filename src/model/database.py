from typing import Annotated

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String
from src.model.ENV import settings


# создаем движок sqlalchemy для работы с БД
# если базы currency_exchange в базе данных нет, то она будет создана, если она есть, то будет создано подключение к ней
async_engine = create_async_engine(url=settings.DATA_BASE_URL, echo=False)
# создаем переменную async_session_factory для создания сессий
async_session_factory = async_sessionmaker(bind=async_engine)

str_3 = Annotated[str, 3]         # тип данных строка длиной до 3 символов
str_50 = Annotated[str, 50]       # тип данных строка длиной до 50 символов


class Base(DeclarativeBase):
    """
    Базовый класс для создания моделей данных, которые представляют таблицы в базе данных.
    """
    type_annotation_map = {
        str_3: String(3),
        str_50: String(50)
    }
