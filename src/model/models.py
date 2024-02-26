import decimal

from sqlalchemy import String, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.database import Base


class Currency(Base):
    __tablename__ = "currencies"

    code: Mapped[str] = mapped_column(String(3), unique=True)
    full_name: Mapped[str] = mapped_column(String(50))
    sign: Mapped[str] = mapped_column(String(3))

    base_exchange_rates = relationship(
        'ExchangeRate',
        foreign_keys='ExchangeRate.base_currency_id',
        back_populates='base_currency',
        cascade='all, delete-orphan'
    )

    target_exchange_rates = relationship(
        'ExchangeRate',
        foreign_keys='ExchangeRate.target_currency_id',
        back_populates='target_currency',
        cascade='all, delete-orphan'
    )


class ExchangeRate(Base):
    __tablename__ = "exchangerates"

    base_currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id", ondelete='CASCADE'))
    target_currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id", ondelete='CASCADE'))
    rate: Mapped[decimal.Decimal] = mapped_column(Numeric(precision=12, scale=4), nullable=False)

    base_currency = relationship(
        'Currency',
        foreign_keys=[base_currency_id],
        back_populates='base_exchange_rates'
    )

    target_currency = relationship(
        'Currency',
        foreign_keys=[target_currency_id],
        back_populates='target_exchange_rates'
    )

    __table_args__ = (UniqueConstraint('base_currency_id', 'target_currency_id', name='unique_id'),)
