from src.dto import CurrencyDTO
from src.model import Currency


class CurrencyService:

    @staticmethod
    def get_currency_dto(currency: Currency) -> CurrencyDTO:
        """
        Метод создает DTO объект на основе объекта модели класса Currency
        :param currency: объект класса Currency
        :return: CurrencyDTO
        """
        currency_dto_obj = CurrencyDTO(
            currency_id=currency.id,
            name=currency.full_name,
            code=currency.code,
            sign=currency.sign,

        )
        return currency_dto_obj


async def currency_service():
    return CurrencyService()
