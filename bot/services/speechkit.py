import asyncio

import aiohttp
from aiogram.types import BufferedInputFile

from bot.config import settings


class SpeechKitService:
    """Сервис для взаимодействия со SpeechKit."""

    def __init__(self):
        self.base_url = settings.SPEECH_KIT_URL
        self.api_key = settings.SPEECH_KIT_API_KEY
        self._cache = {}
        self._cache_lock = asyncio.Lock()

    async def text_to_speech(
            self,
            text: str,
            filename: str
    ) -> BufferedInputFile:
        cache_key = str(hash(text))

        # Проверяем кэш.
        async with self._cache_lock:
            if cache_key in self._cache:
                return BufferedInputFile(
                    self._cache[cache_key],
                    filename=filename
                )

        # Генерируем аудио, если нет в кэше.
        audio_data = await self._synthesize_speech(text)

        # Сохраняем в кэш
        async with self._cache_lock:
            self._cache[cache_key] = audio_data

        return BufferedInputFile(audio_data, filename=filename)

    async def _synthesize_speech(self, text: str) -> bytes:
        """Запрос в SpeechKit на синтез аудио."""

        headers = {
            "Authorization": f"Api-Key {self.api_key}",
        }
        data = {
            "text": text,
            "lang": settings.VOICE_LANG,
            "voice": settings.VOICE_NAME
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.base_url,
                data=data,
                headers=headers
            ) as response:
                if response.status == 200:
                    return await response.read()
                else:
                    raise Exception(
                        f"SpeechKit error: status {response.status}")
