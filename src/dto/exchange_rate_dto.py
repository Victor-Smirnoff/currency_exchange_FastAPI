from pydantic import BaseModel, Field
from src.dto import CurrencyDTO


class ExchangeRateDTO(BaseModel):
    """
    Класс для передачи данных об обменном курсе
    """
    exchange_rate_id: int = Field(..., serialization_alias="id")
    base_currency: CurrencyDTO = Field(..., serialization_alias="baseCurrency")
    target_currency: CurrencyDTO = Field(..., serialization_alias="targetCurrency")
    rate: float = Field(..., serialization_alias="rate")

    class Config:
        arbitrary_types_allowed = True
