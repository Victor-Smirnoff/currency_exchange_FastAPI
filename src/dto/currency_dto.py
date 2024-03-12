from pydantic import BaseModel, Field


class CurrencyDTO(BaseModel):
    """
    Класс для передачи данных о валюте
    """

    currency_id: int = Field(..., serialization_alias="id")
    name: str = Field(..., serialization_alias="name")
    code: str = Field(..., serialization_alias="code")
    sign: str = Field(..., serialization_alias="sign")

    class Config:
        arbitrary_types_allowed = True
