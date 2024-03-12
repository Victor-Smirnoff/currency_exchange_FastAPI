from pydantic import BaseModel, Field
from src.dto import CurrencyDTO


class ExchangeDTO(BaseModel):
    """
    Класс для передачи данных об обмене валюты
    """
    base_currency: CurrencyDTO = Field(..., serialization_alias="baseCurrency")
    target_currency: CurrencyDTO = Field(..., serialization_alias="targetCurrency")
    rate: float = Field(..., serialization_alias="rate")
    amount: int | float = Field(..., serialization_alias="amount")
    converted_amount: float = Field(..., serialization_alias="convertedAmount")

    class Config:
        arbitrary_types_allowed = True
