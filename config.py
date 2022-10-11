from pydantic import BaseSettings
from functools import lru_cache
import socket

hostname = socket.gethostname()
class Settings(BaseSettings):
    env_name: str = "Heroku"
    base_url: str = hostname
    db_url: str = "sqlite:///./shortener.db"
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings