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

Инициировать новый проект для миграций alembic командой<br>
alembic init -t async alembic

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
