"""
Здесь описаны классы кастомных исключений.
Они нужны для возврата корректного ответа в случае ошибки.
"""


class CurrencyException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


class ExchangerateException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
