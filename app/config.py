from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    access_token_expire_minutes: int = 30
    database_url: str = ""
    secret_key: str = ""
    algorithm: str = "HS256"

    model_config = {"env_file": Path(__file__).parent.parent / ".env"}

settings = Settings()