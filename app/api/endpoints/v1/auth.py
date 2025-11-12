import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer

from app.core.config import settings
from app.schemas.auth import LoginRequest


router = APIRouter()

security = HTTPBearer()

active_tokens = set()


def check_auth(token=Depends(security)):
    if token.credentials not in active_tokens:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Предоставлен неверный токен"
        )


@router.post("/login")
def login(login_data: LoginRequest):
    if login_data.username != settings.admin_username or login_data.password != settings.admin_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Предоставлены неверные учётные данные"
        )

    token = secrets.token_hex(16)
    active_tokens.add(token)

    return {"access_token": token, "token_type": "Bearer"}


@router.get("/check_token")
def check_token_is_valid(
    token=Depends(security),
):
    if token.credentials in active_tokens:
        return {"valid": True}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Токен не валиден"
        )
