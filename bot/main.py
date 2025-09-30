import asyncio

from aiogram import Bot, Dispatcher

from bot.config import settings
from database.db_manager import DatabaseManager
from handlers.form_handlers import FormHandlers
from services.speechkit import SpeechKitService
from services.yandex_forms import YandexFormsService


async def main():

    # Инициализируем сервисы и менеджера базы.
    db = DatabaseManager()
    forms_service = YandexFormsService()
    speech_service = SpeechKitService()

    # Инициализируем бота и диспетчер.
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    # Регистрируем обработчики.
    form_handlers = FormHandlers(
        db,
        forms_service=forms_service,
        speech_service=speech_service
    )
    dp.include_router(form_handlers.router)

    # Запускаем поллинг.
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    # Запускаем event_loop.
    asyncio.run(main())
