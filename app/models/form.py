from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Form(Base):
    """Модель формы."""

    name: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"Объект формы. Название: {self.name[:20]}"
