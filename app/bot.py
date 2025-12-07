from aiogram import Bot, Dispatcher

from .config import get_settings
from .handlers import router

settings = get_settings()
bot = Bot(settings.require_token())
dp = Dispatcher()
dp.include_router(router)
