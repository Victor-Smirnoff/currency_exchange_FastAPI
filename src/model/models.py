import decimal

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.model.database import Base


class Currencies(Base):
    code: Mapped[str] = mapped_column(String(3))
    full_name: Mapped[str] = mapped_column(String(50))
    sign: Mapped[str] = mapped_column(String(3))


class ExchangeRates(Base):
    base_currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"))
    target_currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"))
    rate: Mapped[decimal] = mapped_column()
