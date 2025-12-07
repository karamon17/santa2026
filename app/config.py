import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration loaded from environment variables."""

    def __init__(self) -> None:
        self.telegram_token = os.getenv("TELEGRAM_TOKEN", "")
        self.target_score = int(os.getenv("TARGET_SCORE", "15"))

    def require_token(self) -> str:
        if not self.telegram_token:
            raise RuntimeError("TELEGRAM_TOKEN environment variable is not set")
        return self.telegram_token


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
