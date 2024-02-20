"""
Здесь описан класс для хранения данных по ответу с какой-либо ошибкой
"""


class ErrorResponse:
    """
    Класс для хранения данных по ответу с какой-либо ошибкой
    """
    def __init__(self, code, message):
        """
        :param code: код HTTP ответа
        :param message: сообщение ответа
        """
        self.code = code
        self.message = message

    def __str__(self):
        return str({"message": self.message, "code": self.code})