import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "postgresql+asyncpg://tks_admin:changeme@localhost:5432/tks_colours"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:4173"]
    APP_ENV: str = "development"
    SECRET_KEY: str = "change-this-in-production"

    # Email
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = "noreply@school.edu"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_FROM_NAME: str = "TKS Colours"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Automatically add Vercel deployment URLs to CORS when deployed
        vercel_url = os.environ.get("VERCEL_URL")
        if vercel_url:
            self.CORS_ORIGINS = list(self.CORS_ORIGINS) + [
                f"https://{vercel_url}",
            ]


settings = Settings()

