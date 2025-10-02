# Стек технологий
<div id="badges" align="center">
  <img src="https://img.shields.io/badge/Python%203.11-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/>
  <img src="https://img.shields.io/badge/FastAPI%20-white?style=for-the-badge&logo=fastapi&"/>
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white"/>
  <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"/>
  <img src="https://img.shields.io/badge/Aiogram-black?style=for-the-badge&logo=aiogram&logoColor=white"/>
</div>

# Описание проекта
## Возможности
Проект включает голосового бота и бэкенд-сервис, позволяющий незрячим людям самостоятельно проходить опросы. Бот озвучивает вопросы и варианты ответов, принимает голосовые команды и подтверждает выбор. Бэкенд-система обеспечивает удобную загрузку форм, хранение структуры опросов и генерацию уникальных ссылок на бота для прохождения конкретного опроса.
## Функциональность бота
- Озвучивание вопросов и ответов с помощью синтеза речи.
- Подтверждение и отправка ответов с обратной аудиосвязью.
- Работа с разными типами вопросов (одиночный/множественный выбор, текстовые ответы, шкалы).
- Доступность на мобильных устройствах и компьютере.
## Функциональность бэкенда
- Загрузка форм опросов в различных форматах.
- Хранение и управление вопросниками.
- Генерация уникальных ссылок для подключения к боту и прохождения конкретного опроса.
## Технологии
- TTS (Text-to-Speech) для озвучивания - Yandex SpeechKit.
- Интеграция с мессенджерами Telegram.
## Целевая аудитория
Незрячие и слабовидящие пользователи, исследовательские центры, организации и компании, проводящие опросы и анкетирования.

# Установка проекта.

## Установка проекта из репозитория  GitHub.
### Установить Python 3.11

<details>
  <summary>Windows</summary>
https://www.python.org/downloads/
</details>

<details>
  <summary>Linux & MacOS</summary>
  
```bash
  sudo apt update
  sudo apt -y install python3-pip
  sudo apt install python3.11
```

</details>

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
