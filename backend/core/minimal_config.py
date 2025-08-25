"""Minimal configuration for quick start development."""

import os
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class MinimalSettings(BaseSettings):
    """Minimal settings for quick start - only essential configs."""

    # App basics
    app_name: str = Field(default="LumaEngine", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    debug: bool = Field(default=True, alias="DEBUG")

    # Server config
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    reload: bool = Field(default=True, alias="RELOAD")

    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_file: Optional[str] = Field(default=None, alias="LOG_FILE")

    # API
    api_prefix: str = Field(default="/api/v1", alias="API_PREFIX")

    # CORS - minimal for local dev
    cors_origins: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:8000",
        ],
        alias="CORS_ORIGINS",
    )
    cors_methods: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE"], alias="CORS_METHODS"
    )
    cors_headers: List[str] = Field(default=["*"], alias="CORS_HEADERS")

    # Features - all disabled for minimal setup
    enable_metrics: bool = Field(default=False, alias="ENABLE_METRICS")
    enable_tracing: bool = Field(default=False, alias="ENABLE_TRACING")
    enable_caching: bool = Field(default=False, alias="ENABLE_CACHING")
    enable_rate_limiting: bool = Field(default=False, alias="ENABLE_RATE_LIMITING")

    # Environment helpers
    @property
    def is_development(self) -> bool:
        return self.environment.lower() == "development"

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    class Config:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
settings = MinimalSettings()
