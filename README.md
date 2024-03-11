# Проект “Обмен валют” на FastAPI

REST API для описания валют и обменных курсов. Позволяет просматривать и редактировать списки валют и обменных курсов, и совершать расчёт конвертации произвольных сумм из одной валюты в другую.

Веб-интерфейс для проекта не подразумевается.

[Техническое задание проекта](https://zhukovsd.github.io/python-backend-learning-course/Projects/CurrencyExchange/)

## Реализация проекта с использованием следующих технологиий:
![Python](https://img.shields.io/badge/Python-333?style=for-the-badge&logo=python&logoColor=yellow)
![FastAPI](https://img.shields.io/badge/FastAPI-333?style=for-the-badge&logo=FastAPI&logoColor=#009688)
![Asyncio](https://img.shields.io/badge/Asyncio-333?style=for-the-badge&logo=Asyncio)

![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-333?style=for-the-badge&logo=SQLAlchemy)
![Alembic](https://img.shields.io/badge/Alembic-333?style=for-the-badge&logo=Alembic)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-333?style=for-the-badge&logo=PostgreSQL)

![Uvicorn](https://img.shields.io/badge/Uvicorn-333?style=for-the-badge&logo=Uvicorn)
![Poetry](https://img.shields.io/badge/Poetry-333?style=for-the-badge&logo=Poetry)

## Мотивация:

Реализация приложения в асинхронном стиле с использованием Asyncio<br>
Использование веб-фреймворка FastAPI<br>
Использование фреймворка для БД SQLAlchemy<br>
Работа с СУБД PostgreSQL<br>
Выполнение миграций через Alembic<br>
Управление зависимостями через Poetry<br>

## Для успешного запуска приложения:

Найти и арендовать сервер или можно запустить локально

Клонировать этот репозиторий

Установить СУБД PostgreSQL, создать в ней новую БД с именем "currency_exchange", создать пользователя с именем "currency_user", установить разрешения для этого пользователя, установить пароль "0000"

Создать виртуальное окружение для проекта.

Установить poetry командой<br>
pip install poetry

Установить python = "^3.12" и все зависимости из файла pyproject.toml командой<br>
poetry install<br>
или с использованием pip командой<br>
pip install -r pyproject.toml

Удалить все файлы и директории alembic<br>

Инициировать новый проект для миграций alembic командой<br>
alembic init -t async alembic

Скопировать содержимое файлов настроек конфигурации alembic.ini и env.py из данного репозитория во вновь созданные файлы<br>

Выполнить начальную миграцию через alembic командой<br>
alembic revision --autogenerate -m "tables creation"

Применить миграцию командой<br>
alembic upgrade head

После успешной миграции выполнить наполнение таблиц БС тестовыми данными. Для этого запустить файл src/model/insert_data_for_db.py

После наполнения БД тестовыми данными можно запустить файл main.py из директории src

После запуска файла main.py можно пробовать обращаться к эндпоинтам по адресу<br>
http://127.0.0.1:8000

Автоматически созднанная документация по всем эндпоинтам будет доступна по адресу<br>
http://127.0.0.1:8000/docs

## REST API

#### GET `/currencies`

Получение списка валют. Пример ответа:
```
[
    {
        "id": 0,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },   
    {
        "id": 0,
        "name": "Euro",
        "code": "EUR",
        "sign": "€"
    }
]
```

HTTP коды ответов:
- Успех - 200
- Ошибка (например, база данных недоступна) - 500

#### GET `/currency/EUR`

Получение конкретной валюты. Пример ответа:
```
{
    "id": 0,
    "name": "Euro",
    "code": "EUR",
    "sign": "€"
}
```

HTTP коды ответов:
- Успех - 200
- Код валюты отсутствует в адресе - 400
- Валюта не найдена - 404
- Ошибка (например, база данных недоступна) - 500

#### POST `/currencies`

Добавление новой валюты в базу. Данные передаются в теле запроса в виде полей формы (`x-www-form-urlencoded`). Поля формы - `name`, `code`, `sign`. Пример ответа - JSON представление вставленной в базу записи, включая её ID:
```
{
    "id": 0,
    "name": "Euro",
    "code": "EUR",
    "sign": "€"
}
```

HTTP коды ответов:
- Успех - 200
- Отсутствует нужное поле формы - 400
- Валюта с таким кодом уже существует - 409
- Ошибка (например, база данных недоступна) - 500

### Обменные курсы

#### GET `/exchangeRates`

Получение списка всех обменных курсов. Пример ответа:
```
[
    {
        "id": 0,
        "baseCurrency": {
            "id": 0,
            "name": "United States dollar",
            "code": "USD",
            "sign": "$"
        },
        "targetCurrency": {
            "id": 1,
            "name": "Euro",
            "code": "EUR",
            "sign": "€"
        },
        "rate": 0.99
    }
]
```

HTTP коды ответов:
- Успех - 200
- Ошибка (например, база данных недоступна) - 500

#### GET `/exchangeRate/USDRUB`

Получение конкретного обменного курса. Валютная пара задаётся идущими подряд кодами валют в адресе запроса. Пример ответа:
```
{
    "id": 0,
    "baseCurrency": {
        "id": 0,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },
    "targetCurrency": {
        "id": 1,
        "name": "Euro",
        "code": "EUR",
        "sign": "€"
    },
    "rate": 0.99
}

```

HTTP коды ответов:
- Успех - 200
- Коды валют пары отсутствуют в адресе - 400
- Обменный курс для пары не найден - 404
- Ошибка (например, база данных недоступна) - 500

#### POST `/exchangeRates`

Добавление нового обменного курса в базу. Данные передаются в теле запроса в виде полей формы (`x-www-form-urlencoded`). Поля формы - `baseCurrencyCode`, `targetCurrencyCode`, `rate`. Пример полей формы:
- `baseCurrencyCode` - USD
- `targetCurrencyCode` - EUR
- `rate` - 0.99

Пример ответа - JSON представление вставленной в базу записи, включая её ID:
```
{
    "id": 0,
    "baseCurrency": {
        "id": 0,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },
    "targetCurrency": {
        "id": 1,
        "name": "Euro",
        "code": "EUR",
        "sign": "€"
    },
    "rate": 0.99
}
```

HTTP коды ответов:
- Успех - 200
- Отсутствует нужное поле формы - 400
- Валютная пара с таким кодом уже существует - 409
- Одна (или обе) валюта из валютной пары не существует в БД - 404
- Ошибка (например, база данных недоступна) - 500

#### PATCH `/exchangeRate/USDRUB`

Обновление существующего в базе обменного курса. Валютная пара задаётся идущими подряд кодами валют в адресе запроса. Данные передаются в теле запроса в виде полей формы (`x-www-form-urlencoded`). Единственное поле формы - `rate`.

Пример ответа - JSON представление обновлённой записи в базе данных, включая её ID:
```
{
    "id": 0,
    "baseCurrency": {
        "id": 0,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },
    "targetCurrency": {
        "id": 1,
        "name": "Euro",
        "code": "EUR",
        "sign": "€"
    },
    "rate": 0.99
}

```

HTTP коды ответов:
- Успех - 200
- Отсутствует нужное поле формы - 400
- Валютная пара отсутствует в базе данных - 404
- Ошибка (например, база данных недоступна) - 500

### Обмен валюты

#### GET `/exchange?from=BASE_CURRENCY_CODE&to=TARGET_CURRENCY_CODE&amount=$AMOUNT`

Расчёт перевода определённого количества средств из одной валюты в другую. Пример запроса - GET `/exchange?from=USD&to=AUD&amount=10`.

Пример ответа:
```
{
    "baseCurrency": {
        "id": 0,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },
    "targetCurrency": {
        "id": 1,
        "name": "Australian dollar",
        "code": "AUD",
        "sign": "A€"
    },
    "rate": 1.45,
    "amount": 10.00
    "convertedAmount": 14.50
}
```
---

Для всех запросов, в случае ошибки, ответ может выглядеть так:
```
{
    "message": "Валюта не найдена"
}
```
