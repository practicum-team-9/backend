from fastapi import Query
from typing import Optional


def pagination_params(
    skip: int = Query(
        0,
        ge=0,
        title="Пропустить",
        description="Сколько записей пропустить с начала (минимум 0)"
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        title="Лимит",
        description="Сколько записей вернуть за один запрос (от 1 до 100)"
    )
):
    return {"skip": skip, "limit": limit}


def filter_params(
    search: Optional[str] = Query(
        None,
        title="Поиск",
        description="Поиск по имени формы (без учёта регистра)"
    ),
    sort_desc: bool = Query(
        False,
        title="Сортировка по ID",
        description=(
            "True — сортировка по убыванию по ID, "
            "False — по возрастанию"
        )
    )
):
    return {"search": search, "sort_desc": sort_desc}
