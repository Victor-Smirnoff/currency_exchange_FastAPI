from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """
    Класс для хранения данных по ответу с какой-либо ошибкой
    """

    code: int
    message: str

    def __str__(self):
        return str({"message": self.message, "code": self.code})
