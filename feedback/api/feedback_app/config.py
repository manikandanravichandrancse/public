"""
Configuration module for the Feedback API.

Manages environment variables and application settings
using Pydantic Settings for validation and type safety.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        database_url (str): Database connection string
        api_title (str): API title for documentation
        api_version (str): API version
        allowed_origins (List[str]): CORS allowed origins
        host (str): Server host
        port (int): Server port
        reload (bool): Enable auto-reload in development
    """

    # Database
    database_url: str

    # API Info
    api_title: str
    api_version: str
    api_description: str

    # CORS
    allowed_origins: str

    # Server
    host: str
    port: int
    reload: bool

    # Pagination
    default_page_size: int = 100
    max_page_size: int = 1000

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )

    def get_cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        if self.allowed_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.allowed_origins.split(",")]


# Global settings instance
settings = Settings()
