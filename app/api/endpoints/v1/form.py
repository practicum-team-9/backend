from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.form import FormCreate, FormDB, FormUpdate
from app.crud.form import form_crud
from app.core.db import get_async_session
from app.api.validators import validate_form_exists
from app.services.service import get_forms
from app.api.common_params import pagination_params, filter_params

router = APIRouter()




@router.get(
    "/get-all-forms/",
    response_model=list[FormDB],
    summary="Получить все формы"
)
async def get_all_forms(
    session: AsyncSession = Depends(get_async_session),
    pagination: dict = Depends(pagination_params),
    filters: dict = Depends(filter_params)
):
    return await get_forms(session, **pagination, **filters)


@router.post(
    "/add-form/",
    response_model=FormDB,
    summary="Добавить новую форму"
)
async def add_form(
    form: FormCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await form_crud.create(form, session)


@router.delete(
    "/delete-form/{form_id}",
    summary="Удалить форму по ID"
)
async def delete_form(
    form: FormDB = Depends(validate_form_exists),
    session: AsyncSession = Depends(get_async_session)
):
    await form_crud.remove(form, session)
    return {"detail": f"Форма с id={form.id} успешно удалена"}


@router.put(
    "/update-form/{form_id}",
    response_model=FormDB,
    summary="Обновить форму по ID"
)
async def update_form(
    form_update: FormUpdate,
    form: FormDB = Depends(validate_form_exists),
    session: AsyncSession = Depends(get_async_session)
):
    return await form_crud.update(form, form_update, session)


@router.get(
    "/get-form/{form_id}",
    response_model=FormDB,
    summary="Получить форму по ID"
)
async def get_form(
    form: FormDB = Depends(validate_form_exists),
):
    return form