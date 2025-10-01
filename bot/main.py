import asyncio

from aiogram import Bot, Dispatcher
from database.db_manager import DatabaseManager
from handlers.form_handlers import FormHandlers
from services.speechkit import SpeechKitService
from services.yandex_forms import YandexFormsService

from bot.config import settings


async def main():
    """Точка входа. Инициализируем все необходимые сервисы и запускаем бота."""

    db = DatabaseManager()
    forms_service = YandexFormsService()
    speech_service = SpeechKitService()

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    form_handlers = FormHandlers(
        db,
        forms_service=forms_service,
        speech_service=speech_service
    )
    dp.include_router(form_handlers.router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
