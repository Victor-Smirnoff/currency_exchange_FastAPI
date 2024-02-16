import decimal
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DECIMAL
from src.model.database import Base, str_3, str_50
from typing import Annotated

# тип данных int primary_key и autoincrement
int_pk_ai = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
# тип данных int ForeignKey для currencies.ID
currency_id = Annotated[int, mapped_column(ForeignKey("currencies.ID", ondelete="CASCADE"), nullable=False)]


class CurrencyOrm(Base):
    """
    Класс, представляющий таблицу currencies в SQLAlchemy
    """
    __tablename__ = "currencies"

    ID: Mapped[int_pk_ai]
    Code: Mapped[str_3] = mapped_column(nullable=False, unique=True)
    FullName: Mapped[str_50] = mapped_column(nullable=False)
    Sign: Mapped[str_3] = mapped_column(nullable=False, default='¤')

    def __str__(self):
        return f"{self.__class__.__name__}(ID={self.ID}, Code={self.Code}, FullName={self.FullName}, Sign={self.Sign})"


class ExchangeRateOrm(Base):
    """
    Класс, представляющий таблицу exchangerates в SQLAlchemy
    """
    __tablename__ = "exchangerates"

    ID: Mapped[int_pk_ai]
    BaseCurrencyId: Mapped[currency_id] = mapped_column(ForeignKey('currencies.ID'), nullable=False)
    TargetCurrencyId: Mapped[currency_id] = mapped_column(ForeignKey('currencies.ID'), nullable=False)
    Rate: Mapped[decimal] = mapped_column(DECIMAL, nullable=False)

    def __str__(self):
        return (f"{self.__class__.__name__}(ID={self.ID}, BaseCurrencyId={self.BaseCurrencyId}, "
                f"TargetCurrencyId={self.TargetCurrencyId}, Rate={self.Rate})")
