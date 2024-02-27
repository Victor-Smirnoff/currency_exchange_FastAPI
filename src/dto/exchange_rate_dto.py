import decimal

from src.dto import CurrencyDTO


class ExchangeRateDTO:
    """
    Класс для передачи данных об обменном курсе
    """
    def __init__(self, exchange_rate_id: int, base_currency: CurrencyDTO, target_currency: CurrencyDTO, rate: decimal.Decimal):
        self.id = exchange_rate_id
        self.baseCurrency = base_currency
        self.targetCurrency = target_currency
        self.rate = rate
