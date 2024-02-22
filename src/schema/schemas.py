from pydantic import BaseModel


class CurrencyBase(BaseModel):
    code: str
    name: str
    sign: str


class CurrencyCreate(CurrencyBase):
    pass


class Currency(CurrencyBase):
    id: int
