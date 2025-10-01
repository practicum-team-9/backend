from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from bot.config import settings

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


class DatabaseManager:
    """Класс для работы с базой данных."""

    def __init__(self):
        self.session_factory = AsyncSessionLocal

    async def get_form_by_identifier(self, identifier: str) -> dict:
        """Получаем форму по идентификатору из URL"""

        query = text("SELECT * FROM yandexform WHERE url LIKE :identifier")

        async with self.session_factory() as session:
            result = await session.execute(query, {"identifier": f"%{identifier}%"})
            rows = result.fetchall()

            return dict(rows[0]._mapping)
