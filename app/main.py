from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_title,
    description=settings.description,
    docs_url="/docs/v1"
)

app.include_router(main_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        port=8001,
        reload=True
    )
