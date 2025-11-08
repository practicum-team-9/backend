from fastapi import APIRouter

from app.api.endpoints.v1 import form as form_v1
from app.api.endpoints.v1.auth import router as auth_router


main_router = APIRouter()
main_router.include_router(
    form_v1.router,
    prefix="/v1/forms",
    tags=["Forms v1"]
)
main_router.include_router(
    auth_router,
    prefix="/v1/auth",
    tags=["Auth"]
)
