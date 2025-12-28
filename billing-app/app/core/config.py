"""Configuration settings for the billing application."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    database_url: str
    secret_key: str = "change-me-in-production"
    email_smtp_server: str = "smtp.gmail.com"
    email_smtp_port: int = 587
    email_username: str
    email_password: str

    class Config:
        """Pydantic configuration."""

        env_file = ".env"


settings = Settings()
