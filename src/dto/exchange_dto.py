import decimal

from src.dto import CurrencyDTO


class ExchangeDTO:
    """
    Класс для передачи данных об обмене валюты
    """
    def __init__(
            self,
            baseCurrency: CurrencyDTO,
            targetCurrency: CurrencyDTO,
            rate: decimal.Decimal,
            amount: float,
            convertedAmount: float,
            ):
        self.baseCurrency = baseCurrency
        self.targetCurrency = targetCurrency
        self.rate = rate
        self.amount = amount
        self.convertedAmount = convertedAmount
