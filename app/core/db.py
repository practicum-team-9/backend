"""Базовые настройки моделей БД, асинхронного движка и асинхронной сессии."""
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import (
    declarative_base, declared_attr, Mapped, mapped_column, sessionmaker
)


from app.core.config import settings


class PreBase:
    """
    Класс-шаблон для всех моделей БД.
    Определяем, что название таблицы будет формироваться из названия класса.
    Определяем, что в каждой таблице по дефолту будет поле id.
    """
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(
        primary_key=True,
        unique=True,
        autoincrement=True,
        index=True
    )


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session