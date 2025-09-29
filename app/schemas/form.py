from pydantic import BaseModel


class FormBase(BaseModel):
    name: str
    url: str


class FormCreate(FormBase):
    """Схема для создания формы"""
    pass


class FormDB(FormBase):
    """Схема для возврата формы из БД"""
    id: int

    class Config:
        orm_mode = True
