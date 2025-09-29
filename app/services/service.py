from sqlalchemy import select, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.models.form import YandexForm


async def get_forms(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    sort_desc: bool = False
):
    """
    Получить список форм из базы данных с поддержкой поиска,
    сортировки и пагинации
    """
    q = select(YandexForm)

    if search:
        q = q.where(YandexForm.name.ilike(f"%{search}%"))

    column = YandexForm.id
    q = q.order_by(desc(column) if sort_desc else asc(column))

    q = q.offset(skip).limit(limit)

    result = await session.execute(q)
    return result.scalars().all()
