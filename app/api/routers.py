from fastapi import APIRouter

from app.api.endpoints.v1 import form as form_v1


main_router = APIRouter()
main_router.include_router(
    form_v1.router,
    prefix="/v1/forms",
    tags=["Forms v1"]
)
