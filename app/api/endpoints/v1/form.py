from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.form import FormCreate, FormDB, FormUpdate, FormWithURLs
from app.crud.form import form_crud
from app.core.db import get_async_session
from app.api.validators import validate_form_exists
from app.services.service import get_forms
from app.api.common_params import pagination_params, filter_params
from app.api.utils import generate_self_url, generate_tg_url

router = APIRouter()


@router.get(
    "/get-all-forms/",
    response_model=list[FormWithURLs],
    summary="Получить все формы"
)
async def get_all_forms(
    session: AsyncSession = Depends(get_async_session),
    pagination: dict = Depends(pagination_params),
    filters: dict = Depends(filter_params)
):
    result = []
    all_forms = await get_forms(session, **pagination, **filters)
    for form in all_forms:
        identifier = form.url.split("/")[-2]
        result.append(
            FormWithURLs(
                self_page_path=await generate_self_url(form.id),
                tg_bot_url=await generate_tg_url(identifier),
                **form.__dict__,
            )
        )
    return result


@router.post(
    "/add-form/",
    response_model=FormWithURLs,
    summary="Добавить новую форму"
)
async def add_form(
    form: FormCreate,
    session: AsyncSession = Depends(get_async_session)
):
    new_form = await form_crud.create(form, session)
    identifier = new_form.url.split("/")[-2]
    return FormWithURLs(
        self_page_path=await generate_self_url(new_form.id),
        tg_bot_url=await generate_tg_url(identifier),
        **new_form.__dict__,
    )



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
    response_model=FormWithURLs,
    summary="Обновить форму по ID"
)
async def update_form(
    form_update: FormUpdate,
    form: FormDB = Depends(validate_form_exists),
    session: AsyncSession = Depends(get_async_session)
):
    updated_form = await form_crud.update(form, form_update, session)
    identifier = updated_form.url.split("/")[-2]
    return FormWithURLs(
        self_page_path=await generate_self_url(updated_form.id),
        tg_bot_url=await generate_tg_url(identifier),
        **updated_form.__dict__,
    )


@router.get(
    "/get-form/{form_id}",
    response_model=FormWithURLs,
    summary="Получить форму по ID"
)
async def get_form(
    form: FormWithURLs = Depends(validate_form_exists)
):
    identifier = form.url.split("/")[-2]
    form.tg_bot_url = await generate_tg_url(identifier)
    form.self_page_path = await generate_self_url(form.id)
    return form
