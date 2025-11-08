from pydantic import BaseModel


class LoginRequest(BaseModel):
    """Схема запроса на логин."""
    username: str
    password: str
