from decimal import getcontext, Decimal

from src.dao import DaoExchangeRepository, DaoCurrencyRepository
from src.dto import ExchangeResponse, ErrorResponse, ExchangeDTO
from src.model import ExchangeRate
from src.service.currency_service import CurrencyService


class ExchangeService:
    """
    Класс для выполнения бизнес-логики получения расчёта
    перевода определённого количества средств из одной валюты в другую
    """

    async def convert_currency(
        self,
        currency_from: str,
        currency_to: str,
        amount: float,
        dao_currency_obj: DaoCurrencyRepository,
        dao_exchange_obj: DaoExchangeRepository,
    ) -> ExchangeResponse | ErrorResponse:
        """
        Метод принимает в обработку запрос на расчёт перевода определённого количества средств из одной валюты в другую
        :param currency_from: из какой валюты перевод (базовая валюта)
        :param currency_to: в какую валюту перевод (целевая валюта)
        :param amount: количество базовой валюты
        :param dao_currency_obj: здесь передается зависимость на объект класса DaoCurrencyRepository
        :param dao_exchange_obj: здесь передается зависимость на объект класса DaoExchangeRepository
        :return: объект класса ExchangeResponse или объект класса ErrorResponse
        """
        # пробуем получить прямой курс и конвертировать
        response = await self.get_direct_course(
            currency_from=currency_from,
            currency_to=currency_to,
            amount=amount,
            dao_currency_obj=dao_currency_obj,
            dao_exchange_obj=dao_exchange_obj
        )
        if isinstance(response, ExchangeResponse):
            return response

        # пробуем получить обратный курс и конвертировать
        response = await self.get_reverse_course(
            currency_from=currency_from,
            currency_to=currency_to,
            amount=amount,
            dao_currency_obj=dao_currency_obj,
            dao_exchange_obj=dao_exchange_obj
        )
        if isinstance(response, ExchangeResponse):
            return response

        # пробуем получить кросс-курс и конвертировать
        response = await self.get_cross_course(
            currency_from=currency_from,
            currency_to=currency_to,
            amount=amount,
            dao_currency_obj=dao_currency_obj,
            dao_exchange_obj=dao_exchange_obj
        )
        if isinstance(response, ExchangeResponse):
            return response

        # если пришли сюда и ничего не вернули, то возвращаем message Обменный курс не найден
        return response

    @staticmethod
    async def get_direct_course(
        currency_from: str,
        currency_to: str,
        amount: float,
        dao_currency_obj: DaoCurrencyRepository,
        dao_exchange_obj: DaoExchangeRepository,
    ) -> ExchangeResponse | ErrorResponse:
        """
        Метод пытается найти прямой обменный курс, если находит, то возвращает объект класса ExchangeResponse
        или объект класса ErrorResponse - если нет прямого обменного курса
        :param currency_from: из какой валюты перевод (базовая валюта)
        :param currency_to: в какую валюту перевод (целевая валюта)
        :param amount: количество базовой валюты
        :param dao_currency_obj: здесь передается зависимость на объект класса DaoCurrencyRepository
        :param dao_exchange_obj: здесь передается зависимость на объект класса DaoExchangeRepository
        :return: объект класса ExchangeResponse или объект класса ErrorResponse
        """
        getcontext().prec = 7  # устанавливаем точность числа в 7 знаков
        amount = Decimal(amount)

        # пробуем получить данные по прямому этому курсу валют
        response = await dao_exchange_obj.find_by_codes(
            base_currency_code=currency_from,
            target_currency_code=currency_to,
        )
        if isinstance(response, ExchangeRate):
            base_currency_id = response.base_currency_id
            target_currency_id = response.target_currency_id
            rate = response.rate
            converted_amount = Decimal(rate) * amount
            converted_amount = str(converted_amount.quantize(Decimal('1.00')))  # округление до 2 цифр в дробной части
            base_currency = await dao_currency_obj.find_by_id(
                currency_id=base_currency_id,
            )
            target_currency = await dao_currency_obj.find_by_id(
                currency_id=target_currency_id,
            )
            amount = str(amount)
            response = ExchangeResponse(base_currency, target_currency, rate, amount, converted_amount)
            return response
        else:
            return response

    @staticmethod
    async def get_reverse_course(
        currency_from: str,
        currency_to: str,
        amount: float,
        dao_currency_obj: DaoCurrencyRepository,
        dao_exchange_obj: DaoExchangeRepository,
    ) -> ExchangeResponse | ErrorResponse:
        """
        Метод пытается найти обратный обменный курс, если находит, то возвращает объект класса ExchangeResponse
        или объект класса ErrorResponse - если нет обратного обменного курса
        :param currency_from: из какой валюты перевод (базовая валюта)
        :param currency_to: в какую валюту перевод (целевая валюта)
        :param amount: количество базовой валюты
        :param dao_currency_obj: здесь передается зависимость на объект класса DaoCurrencyRepository
        :param dao_exchange_obj: здесь передается зависимость на объект класса DaoExchangeRepository
        :return: объект класса ExchangeResponse или объект класса ErrorResponse
        """
        getcontext().prec = 7  # устанавливаем точность числа в 7 знаков
        amount = Decimal(amount)

        # пробуем получить данные по обратному курсу валют
        response = await dao_exchange_obj.find_by_codes(
            base_currency_code=currency_to,
            target_currency_code=currency_from,
        )
        if isinstance(response, ExchangeRate):
            base_currency_id = response.target_currency_id  # base_currency_id в обратном курсе TargetCurrencyId
            target_currency_id = response.base_currency_id  # target_currency_id в обратном курсе BaseCurrencyId
            rate = 1 / Decimal(response.rate)
            rate = str(rate.quantize(Decimal('1.000000')))
            converted_amount = (Decimal(rate)) * amount
            converted_amount = str(converted_amount.quantize(Decimal('1.00')))  # округление до 2 цифр в дробной части
            base_currency = await dao_currency_obj.find_by_id(
                currency_id=base_currency_id,
            )
            target_currency = await dao_currency_obj.find_by_id(
                currency_id=target_currency_id,
            )
            amount = str(amount)
            response = ExchangeResponse(base_currency, target_currency, rate, amount, converted_amount)
            return response
        else:
            return response

    @staticmethod
    async def get_cross_course(
        currency_from: str,
        currency_to: str,
        amount: float,
        dao_currency_obj: DaoCurrencyRepository,
        dao_exchange_obj: DaoExchangeRepository,
    ) -> ExchangeResponse | ErrorResponse:
        """
        Метод пытается найти кросс-курс через USD-валюту, если находит, то возвращает объект класса ExchangeResponse
        или объект класса ErrorResponse - если нет обратного обменного курса
        :param currency_from: из какой валюты перевод (базовая валюта)
        :param currency_to: в какую валюту перевод (целевая валюта)
        :param amount: количество базовой валюты
        :param dao_currency_obj: здесь передается зависимость на объект класса DaoCurrencyRepository
        :param dao_exchange_obj: здесь передается зависимость на объект класса DaoExchangeRepository
        :return: объект класса ExchangeResponse или объект класса ErrorResponse
        """
        getcontext().prec = 7  # устанавливаем точность числа в 7 знаков
        amount = Decimal(amount)
        response_base_currency = await dao_exchange_obj.find_by_codes(
            base_currency_code="USD",
            target_currency_code=currency_from,
        )
        response_target_currency = await dao_exchange_obj.find_by_codes(
            base_currency_code="USD",
            target_currency_code=currency_to,
        )
        if isinstance(response_base_currency, ExchangeRate) and isinstance(response_target_currency, ExchangeRate):
            base_currency_id = response_base_currency.target_currency_id
            target_currency_id = response_target_currency.target_currency_id
            rate = Decimal(response_target_currency.rate) / Decimal(response_base_currency.rate)
            converted_amount = rate * amount
            converted_amount = str(converted_amount.quantize(Decimal('1.00')))  # округление до 2 цифр в дробной части
            rate = str(rate.quantize(Decimal('1.000000')))
            base_currency = await dao_currency_obj.find_by_id(
                currency_id=base_currency_id,
            )
            target_currency = await dao_currency_obj.find_by_id(
                currency_id=target_currency_id,
            )
            amount = str(amount)
            response = ExchangeResponse(base_currency, target_currency, rate, amount, converted_amount)
            return response
        else:
            response_code = 404
            message = f"Ошибка {response_code} - Обменный курс {currency_from}-{currency_to} не найден"
            response = ErrorResponse(response_code, message)
            return response

    @staticmethod
    async def get_exchange_dto(
            exchange_obj: ExchangeResponse,
            currency_service_obj: CurrencyService,
    ):
        """
        Метод создает DTO объект на основе объекта класса ExchangeResponse
        :param exchange_obj: объект класса ExchangeResponse
        :param currency_service_obj: здесь передается зависимость на объект класса CurrencyService
        :return: объект класса ExchangeDTO
        """

        base_currency_dto = currency_service_obj.get_currency_dto(exchange_obj.base_currency)
        target_currency_dto = currency_service_obj.get_currency_dto(exchange_obj.target_currency)

        exchange_dto_obj = ExchangeDTO(
            baseCurrency=base_currency_dto,
            targetCurrency=target_currency_dto,
            rate=exchange_obj.rate,
            amount=exchange_obj.amount,
            convertedAmount=exchange_obj.converted_amount,
        )

        return exchange_dto_obj


async def exchange_service():
    return ExchangeService()
