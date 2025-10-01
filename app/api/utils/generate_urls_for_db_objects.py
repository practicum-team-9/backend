from app.core.config import settings


async def generate_tg_url(identifier: str) -> str:
    return settings.tg_bot_url + f"?start={identifier}"


async def generate_self_url(id: int) -> str:
    return settings.self_url + f"/v1/forms/get-form/{id}"
