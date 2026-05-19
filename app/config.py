from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    access_token_expire_minutes: int = 30
    database_url: str = ""
    secret_key: str = ""
    algorithm: str = "HS256"

    # This config will only be used for local dev
    model_config = SettingsConfigDict(
        env_file= Path(__file__).parent.parent / ".env.local",
        extra="ignore"
    )

settings = Settings()