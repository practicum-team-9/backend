from app.core.db import Base
from sqlalchemy import Column, String


class YaForm(Base):
    """Модель для записи подготовленных Яндекс Форм"""

    __tablename__ = 'ya_forms'

    title = Column(String)
    link = Column(String)
