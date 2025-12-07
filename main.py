import asyncio

from app.bot import bot, dp
from app.config import get_settings
from app.server import app


async def run_polling() -> None:
    settings = get_settings()
    if not settings.telegram_token:
        raise RuntimeError("TELEGRAM_TOKEN environment variable is not set")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_polling())
