from decimal import getcontext, Decimal

from src.dao import DaoExchangeRepository, DaoCurrencyRepository
from src.dto import ExchangeResponse, ErrorResponse, ExchangeDTO
from src.model import ExchangeRate


class ExchangeService(DaoExchangeRepository):
    """
    Класс для выполнения бизнес-логики получения расчёта
    перевода определённого количества средств из одной валюты в другую
    """

    async def convert_currency(self, session, currency_from, currency_to, amount):
        """
        Метод принимает в обработку запрос на расчёт перевода определённого количества средств из одной валюты в другую
        :param session: объект асинхронной сессии AsyncSession
        :param currency_from: из какой валюты перевод (базовая валюта)
        :param currency_to: в какую валюту перевод (целевая валюта)
        :param amount: количество базовой валюты
        :return: объект класса ExchangeResponse или объект класса ErrorResponse
        """
        # пробуем получить прямой курс и конвертировать
        response = await self.get_direct_course(
            session=session,
            currency_from=currency_from,
            currency_to=currency_to,
            amount=amount,
        )
        if isinstance(response, ExchangeResponse):
            return response

        # пробуем получить обратный курс и конвертировать
        response = await self.get_reverse_course(
            session=session,
            currency_from=currency_from,
            currency_to=currency_to,
            amount=amount,
        )
        if isinstance(response, ExchangeResponse):
            return response

        # пробуем получить кросс-курс и конвертировать
        response = await self.get_cross_course(
            session=session,
            currency_from=currency_from,
            currency_to=currency_to,
            amount=amount,
        )
        if isinstance(response, ExchangeResponse):
            return response

        # если пришли сюда и ничего не вернули, то возвращаем message Обменный курс не найден
        return response

    async def get_direct_course(self, session, currency_from, currency_to, amount):
        """
        Метод пытается найти прямой обменный курс, если находит, то возвращает объект класса ExchangeResponse
        или объект класса ErrorResponse - если нет прямого обменного курса
        :param session: объект асинхронной сессии AsyncSession
        :param currency_from: из какой валюты перевод (базовая валюта)
        :param currency_to: в какую валюту перевод (целевая валюта)
        :param amount: количество базовой валюты
        :return: объект класса ExchangeResponse или объект класса ErrorResponse
        """
        getcontext().prec = 7  # устанавливаем точность числа в 7 знаков
        amount = Decimal(amount)
        # складываем коды валют в единую строку для запроса прямого курса
        currency_codes = currency_from + currency_to
        # пробуем получить данные по этому курсу валют
        response = await self.find_by_codes(
            session=session,
            currency_codes=currency_codes,
        )
        if isinstance(response, ExchangeRate):
            dao_currency_obj = DaoCurrencyRepository()
            base_currency_id = response.base_currency_id
            target_currency_id = response.target_currency_id
            rate = response.rate
            converted_amount = Decimal(rate) * amount
            converted_amount = str(converted_amount.quantize(Decimal('1.00')))  # округление до 2 цифр в дробной части
            base_currency = await dao_currency_obj.find_by_id(
                session=session,
                currency_id=base_currency_id,
            )
            target_currency = await dao_currency_obj.find_by_id(
                session=session,
                currency_id=target_currency_id,
            )
            amount = str(amount)
            response = ExchangeResponse(base_currency, target_currency, rate, amount, converted_amount)
            return response
        else:
            return response

    async def get_reverse_course(self, session, currency_from, currency_to, amount):
        """
        Метод пытается найти обратный обменный курс, если находит, то возвращает объект класса ExchangeResponse
        или объект класса ErrorResponse - если нет обратного обменного курса
        :param session: объект асинхронной сессии AsyncSession
        :param currency_from: из какой валюты перевод (базовая валюта)
        :param currency_to: в какую валюту перевод (целевая валюта)
        :param amount: количество базовой валюты
        :return: объект класса ExchangeResponse или объект класса ErrorResponse
        """
        getcontext().prec = 7  # устанавливаем точность числа в 7 знаков
        amount = Decimal(amount)
        # складываем коды валют в единую строку для запроса прямого курса
        reversed_currency_codes = currency_to + currency_from
        # пробуем получить данные по этому курсу валют
        response = await self.find_by_codes(
            session=session,
            currency_codes=reversed_currency_codes,
        )
        if isinstance(response, ExchangeRate):
            dao_currency_obj = DaoCurrencyRepository()
            base_currency_id = response.target_currency_id  # base_currency_id в обратном курсе TargetCurrencyId
            target_currency_id = response.base_currency_id  # target_currency_id в обратном курсе BaseCurrencyId
            rate = 1 / Decimal(response.rate)
            rate = str(rate.quantize(Decimal('1.000000')))
            converted_amount = (Decimal(rate)) * amount
            converted_amount = str(converted_amount.quantize(Decimal('1.00')))  # округление до 2 цифр в дробной части
            base_currency = await dao_currency_obj.find_by_id(
                session=session,
                currency_id=base_currency_id,
            )
            target_currency = await dao_currency_obj.find_by_id(
                session=session,
                currency_id=target_currency_id,
            )
            amount = str(amount)
            response = ExchangeResponse(base_currency, target_currency, rate, amount, converted_amount)
            return response
        else:
            return response

    async def get_cross_course(self, session, currency_from, currency_to, amount):
        """
        Метод пытается найти кросс-курс через USD-валюту, если находит, то возвращает объект класса ExchangeResponse
        или объект класса ErrorResponse - если нет обратного обменного курса
        :param session: объект асинхронной сессии AsyncSession
        :param currency_from: из какой валюты перевод (базовая валюта)
        :param currency_to: в какую валюту перевод (целевая валюта)
        :param amount: количество базовой валюты
        :return: объект класса ExchangeResponse или объект класса ErrorResponse
        """
        getcontext().prec = 7  # устанавливаем точность числа в 7 знаков
        amount = Decimal(amount)
        response_base_currency = await self.find_by_codes(
            session=session,
            currency_codes=str("USD" + currency_from),
        )
        response_target_currency = await self.find_by_codes(
            session=session,
            currency_codes=str("USD" + currency_to),
        )
        if isinstance(response_base_currency, ExchangeRate) and isinstance(response_target_currency, ExchangeRate):
            dao_currency_obj = DaoCurrencyRepository()
            base_currency_id = response_base_currency.target_currency_id
            target_currency_id = response_target_currency.target_currency_id
            rate = Decimal(response_target_currency.rate) / Decimal(response_base_currency.rate)
            converted_amount = rate * amount
            converted_amount = str(converted_amount.quantize(Decimal('1.00')))  # округление до 2 цифр в дробной части
            rate = str(rate.quantize(Decimal('1.000000')))
            base_currency = await dao_currency_obj.find_by_id(
                session=session,
                currency_id=base_currency_id,
            )
            target_currency = await dao_currency_obj.find_by_id(
                session=session,
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
    async def get_exchange_dto(exchange_obj: ExchangeResponse):
        """
        Метод создает DTO объект на основе объекта класса ExchangeResponse
        :param exchange_obj: объект класса ExchangeResponse
        :return: объект класса ExchangeDTO
        """

        dao_currency_obj = DaoCurrencyRepository()

        base_currency_dto = dao_currency_obj.get_currency_dto(exchange_obj.base_currency)
        target_currency_dto = dao_currency_obj.get_currency_dto(exchange_obj.target_currency)

        exchange_dto_obj = ExchangeDTO(
            baseCurrency=base_currency_dto,
            targetCurrency=target_currency_dto,
            rate=exchange_obj.rate,
            amount=exchange_obj.amount,
            convertedAmount=exchange_obj.converted_amount,
        )

        return exchange_dto_obj
