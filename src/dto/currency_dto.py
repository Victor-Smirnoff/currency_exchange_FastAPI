class CurrencyDTO:
    """
    Класс для передачи данных о валюте
    """
    def __init__(self, currency_id: int, name: str, code: str, sign: str):
        self.id = currency_id
        self.name = name
        self.code = code
        self.sign = sign
