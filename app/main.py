from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.api.endpoints import form

app = FastAPI(title=settings.app_title)

app.include_router(main_router)
app.include_router(form.router, tags=["Forms"])
