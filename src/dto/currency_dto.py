class CurrencyDTO:
    """
    Класс для передачи данных о валюте
    """
    def __init__(self, id: int, name: str, code: str, sign: str):
        self.id = id
        self.name = name
        self.code = code
        self.sign = sign
