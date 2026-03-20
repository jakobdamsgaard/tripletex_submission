"""Configuration management for Tripletex agent."""

from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # API Configuration
    tripletex_api_url: str = "https://kkpqfuj-amager.tripletex.dev/v2"
    tripletex_session_token: Optional[str] = None
    tripletex_consumer_token: Optional[str] = None
    tripletex_employee_token: Optional[str] = None
    tripletex_company_id: str = "0"

    # LLM Configuration
    llm_provider: str = "openai"  # "openai" or "anthropic"
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

    # Server Configuration
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    api_timeout_seconds: int = 300

    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = "logs/agent.log"

    # Feature Flags
    use_file_attachments: bool = True
    use_vision_for_images: bool = True
    retry_failed_requests: bool = True
    max_retries: int = 3

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
