import decimal

from src.dto import CurrencyDTO


class ExchangeRateDTO:
    """
    Класс для передачи данных об обменном курсе
    """
    def __init__(self, id: int, baseCurrency: CurrencyDTO, targetCurrency: CurrencyDTO, rate: decimal.Decimal):
        self.id = id
        self.baseCurrency = baseCurrency
        self.targetCurrency = targetCurrency
        self.rate = rate
