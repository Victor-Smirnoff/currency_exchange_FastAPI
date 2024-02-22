class ExchangeResponse:
    """
    Класс для хранения данных по расчёту перевода определённого количества средств из одной валюты в другую
    """
    def __init__(self, base_currency, target_currency, rate, amount, converted_amount):
        """
        :param base_currency: объект с данными базовой валюты (объект класса Currency)
        :param target_currency: объект с данными целевой валюты (объект класса Currency)
        :param rate: обменный курс
        :param amount: количество базовой валюты
        :param converted_amount: полученное количество целевой валюты
        """
        self.base_currency = base_currency
        self.target_currency = target_currency
        self.rate = rate
        self.amount = amount
        self.converted_amount = converted_amount
