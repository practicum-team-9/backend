from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.form import FormCreate, FormDB
from app.crud.form import form_crud
from app.core.db import get_async_session

router = APIRouter()


@router.get("/get-all-forms/", response_model=list[FormDB])
async def get_all_forms(session: AsyncSession = Depends(get_async_session)):
    return await form_crud.get_multi(session)


@router.post("/add-form/", response_model=FormDB)
async def add_form(
    form: FormCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await form_crud.create(form, session)


@router.delete("/delete-form/{form_id}")
async def delete_form(
    form_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    form = await form_crud.get_by_id(form_id, session)
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Форма с id={form_id} не найдена"
        )
    await form_crud.remove(form, session)
    return {"detail": f"Форма с id={form_id} успешно удалена"}
