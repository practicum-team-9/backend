from typing import Optional

from pydantic import BaseModel, ConfigDict


class FormBase(BaseModel):
    """Базовая схема формы"""
    name: str
    url: str


class FormCreate(FormBase):
    """Схема для создания формы"""
    pass


class FormDB(FormBase):
    """Схема для возврата формы из БД"""
    id: int

    model_config = ConfigDict(from_attributes=True)


class FormUpdate(BaseModel):
    """Схема для изменения полей формы"""
    name: Optional[str] = None
    description: Optional[str] = None


class FormWithURLs(FormBase):
    """Схема для возврата формы из БД с доп. ссылками."""
    id: int
    tg_bot_url: Optional[str] = None
    self_page_path: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)