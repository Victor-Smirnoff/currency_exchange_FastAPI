import decimal

from sqlalchemy import String, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from src.model.database import Base


class Currency(Base):
    __tablename__ = "currencies"

    code: Mapped[str] = mapped_column(String(3), unique=True)
    full_name: Mapped[str] = mapped_column(String(50))
    sign: Mapped[str] = mapped_column(String(3))


class ExchangeRate(Base):
    __tablename__ = "exchangerates"

    base_currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"))
    target_currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"))
    rate: Mapped[decimal.Decimal] = mapped_column(Numeric(precision=12, scale=4), nullable=False)
