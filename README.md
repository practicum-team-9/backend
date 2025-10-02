# Стек технологий
<div id="badges" align="center">
  <img src="https://img.shields.io/badge/Python%203.11-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/>
  <img src="https://img.shields.io/badge/FastAPI%20-white?style=for-the-badge&logo=fastapi&"/>
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white"/>
  <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"/>
  <img src="https://img.shields.io/badge/style=for-the-badge&logo=aiogram&logoColor=white"/>
</div>

# Описание проекта

### Регистрация и авторизация.
Пользователь имеет возможность зарегистрироваться и авторизоваться в системе. Получить доступ к своему ЛК,
изменить свои данные.

### Импорт данных.
Есть возможность загрузить данные из файлов с расширением csv. Загрузки данных о дилерах, загрузка продуктов заказчика,
загрузка товаров дилера.

### Главная страница.
На главной странице отображаются товары дилеров. Присутствует возможность фильтрации по статусу сопоставления, 
поиска по названию и сортировки товаров по времени и цене.

### Страница сопоставления.
На странице сопоставления отображаются данные выбранного для сопоставления товара дилера, а также варианты предложенные
ML моделью. Количество выводимых вариантов пользователь настраивает самостоятельно, по умолчанию 5.

### Сопоставленные товары.
Сопоставленные товары записываются в базу данных для дальнейшего использования. И доступны на странице сопоставленных товаров.

### Статистика и аналитика. 
Пользователь имеет возможность просмотреть статистику по сопоставлениям за выбранные период времени. Доступны такие параметры как:
общее количество сопоставлений, количество сопоставлений текущего пользователя, пользователя с конкретным ID, сопоставление
по дилеру с ID. Пользователю так же выводится процент выбираемых позиций.

### Логирование.
Реализована система логирование исключений. На уровне проекта в папке logs сохраняются файлы с логами.

### Версионирование.
В проекте реализовано версионирование API. На данный момент доступна версия v1.

# Установка проекта.

## Установка проекта из репозитория  GitHub.
### Установить Python 3.11
- Для Windows https://www.python.org/downloads/
- Для Linux 
```
sudo apt update
sudo apt -y install python3-pip
sudo apt install python3.11
``` 
### Клонировать репозиторий и перейти в него в командной строке.
```bash
   https://github.com/practicum-team-9/backend.git
``` 
###  Развернуть виртуальное окружение.
```bash
python -m venv venv

``` 
<details>
  <summary>Windows</summary>

```bash
    venv\Scripts\activate.bat
``` 
</details>
<details>
  <summary>Linux & MacOS</summary>

```bash
    source venv/bin/activate
``` 
</details>

### Команды для создания миграций
```bash
alembic revision --autogenerate -m "Migration name"
``` 
### Команды для применения миграций
```bash
alembic upgrade head
```
### Запуск приложения и бота.
- В файле .env заполнить данные БД, токенов бота и yandex Speech-Kit. Пример заполнения.
```
# Общая информация о приложении.
APP_TITLE=
DESCRIPTION=
SELF_URL=хост, на котором запущено приложение

# Параметры подключения к Postgres.
POSTGRES_USER=username 
POSTGRES_PASSWORD=password
POSTGRES_DB=db_name
DB_HOST=host
DB_PORT=port
DB_TYPE=postgresql
DB_API=asyncpg

# BOT
BOT_TOKEN=bot_token
TG_BOT_URL=https://t.me/название бота

# Yandex Speech-Kit
SPEECH_KIT_API_KEY=speech_kit_api_key
SPEECH_KIT_URL=speech_kit_url
VOICE_LANG=ru-RU
VOICE_NAME=alena

# Yandex Forms
YANDEX_FORMS_URL=yandex_forms_url
``` 
- Запустить main.py

## Установка через контейнер Docker
### Склонировать репозиторий
```bash
https://github.com/practicum-team-9/backend.git
``` 
### Перейти в папку infra
```bash
cd infra
``` 
### В файле .env заполнить данные БД, токенов бота и yandex Speech-Kit. Пример заполнения.
```
# Общая информация о приложении.
APP_TITLE=
DESCRIPTION=
SELF_URL=хост, на котором запущено приложение

# Параметры подключения к Postgres.
POSTGRES_USER=username 
POSTGRES_PASSWORD=password
POSTGRES_DB=db_name
DB_HOST=host
DB_PORT=port
DB_TYPE=postgresql
DB_API=asyncpg

# BOT
BOT_TOKEN=bot_token
TG_BOT_URL=https://t.me/название бота

# Yandex Speech-Kit
SPEECH_KIT_API_KEY=speech_kit_api_key
SPEECH_KIT_URL=speech_kit_url
VOICE_LANG=ru-RU
VOICE_NAME=alena

# Yandex Forms
YANDEX_FORMS_URL=yandex_forms_url
``` 
### Запустить сборку образа
```bash
sudo docker-compose up -d
``` 

---

### Применить миграции
```bash
docker-compose exec backend alembic upgrade head
``` 
# Документация API первой версии будет доступна по адресу.
```
http://localhost/docs/v1
``` 
