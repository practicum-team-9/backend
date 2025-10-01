from app.core.config import settings


async def generate_urls(identifier: str, id: int) -> dict:
    return {
        "tg_bot_url": settings.tg_bot_url + f"?start={identifier}",
        "self_page_path": settings.self_url + f"/v1/forms/get-form/{id}"
    }
