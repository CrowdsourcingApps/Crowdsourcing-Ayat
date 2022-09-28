from functools import lru_cache

from src.settings.config import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
