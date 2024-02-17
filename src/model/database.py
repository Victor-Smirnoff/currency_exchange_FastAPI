from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.model.config import settings


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(self):
        return f"{self.__name__.lower()}"

    id: Mapped[int] = mapped_column(primary_key=True)


class DataBaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )


db_helper = DataBaseHelper(url=settings.data_base_url, echo=settings.db_echo)