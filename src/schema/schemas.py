import decimal

from pydantic import BaseModel, ConfigDict, Field


class CurrencyBase(BaseModel):
    code: str
    name: str = Field(..., alias="full_name")
    sign: str


class CurrencyCreate(CurrencyBase):
    pass


class Currency(CurrencyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ExchangeRateBase(BaseModel):
    baseCurrency: dict
    targetCurrency: dict
    rate: decimal.Decimal


class ExchangeRateCreate(ExchangeRateBase):
    pass


class ExchangeRate(ExchangeRateBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
