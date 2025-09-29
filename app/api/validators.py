from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.form import form_crud
from app.core.db import get_async_session
from app.schemas.form import FormDB


async def validate_form_exists(
    form_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> FormDB:
    """
    Проверка существования формы по ID.
    Если форма не найдена, выбрасывается HTTPException 404.
    """
    form = await form_crud.get_by_id(form_id, session)
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Форма с id={form_id} не найдена"
        )
    return form
