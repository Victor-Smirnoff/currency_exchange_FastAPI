class CurrencyDTO:
    """
    Класс для передачи данных о валюте
    """
    def __init__(self, id, name, code, sign):
        self.id = id
        self.name = name
        self.code = code
        self.sign = sign
