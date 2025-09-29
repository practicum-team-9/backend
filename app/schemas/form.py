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
