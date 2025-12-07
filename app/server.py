from fastapi import FastAPI, Request
from aiogram.types import Update

from .bot import bot, dp
from .config import get_settings

app = FastAPI(title="Secret Santa Volvo Quiz")


@app.post("/webhook")
async def telegram_webhook(request: Request) -> dict:
    settings = get_settings()
    if not settings.telegram_token:
        return {"status": "missing token"}
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}


@app.get("/")
async def root() -> dict:
    return {"status": "running"}
