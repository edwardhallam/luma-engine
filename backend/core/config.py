"""Configuration management for AI Infrastructure Deployer."""

from typing import Dict, Any, Optional, List
from pydantic import Field, validator
from pydantic_settings import BaseSettings
import os
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = Field("LumaEngine", env="APP_NAME")
    app_version: str = Field("0.1.0", env="APP_VERSION")
    debug: bool = Field(False, env="DEBUG")
    environment: str = Field("development", env="ENVIRONMENT")
    
    # API
    api_prefix: str = Field("/api/v1", env="API_PREFIX")
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8000, env="PORT")
    reload: bool = Field(False, env="RELOAD")
    
    # Database
    database_url: str = Field(..., env="DATABASE_URL")
    database_pool_size: int = Field(5, env="DATABASE_POOL_SIZE")
    database_max_overflow: int = Field(10, env="DATABASE_MAX_OVERFLOW")
    
    # Redis
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    redis_password: Optional[str] = Field(None, env="REDIS_PASSWORD")
    
    # Temporal
    temporal_host: str = Field("localhost:7233", env="TEMPORAL_HOST")
    temporal_namespace: str = Field("default", env="TEMPORAL_NAMESPACE")
    temporal_task_queue: str = Field("aid-deployment", env="TEMPORAL_TASK_QUEUE")
    
    # LLM Providers
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    ollama_base_url: str = Field("http://localhost:11434", env="OLLAMA_BASE_URL")
    
    # LLM Configuration
    llm_primary_provider: str = Field("openai", env="LLM_PRIMARY_PROVIDER")
    llm_fallback_providers: str = Field("anthropic,ollama", env="LLM_FALLBACK_PROVIDERS")
    llm_max_retries: int = Field(3, env="LLM_MAX_RETRIES")
    llm_timeout: int = Field(30, env="LLM_TIMEOUT")
    
    # Infrastructure
    proxmox_host: Optional[str] = Field(None, env="PROXMOX_HOST")
    proxmox_user: Optional[str] = Field(None, env="PROXMOX_USER")
    proxmox_password: Optional[str] = Field(None, env="PROXMOX_PASSWORD")
    proxmox_verify_ssl: bool = Field(False, env="PROXMOX_VERIFY_SSL")
    
    # GitLab
    gitlab_url: Optional[str] = Field(None, env="GITLAB_URL")
    gitlab_token: Optional[str] = Field(None, env="GITLAB_TOKEN")
    gitlab_project_namespace: str = Field("aid-deployments", env="GITLAB_PROJECT_NAMESPACE")
    
    # MinIO/Object Storage
    minio_endpoint: str = Field("localhost:9000", env="MINIO_ENDPOINT")
    minio_access_key: str = Field("minioadmin", env="MINIO_ACCESS_KEY")
    minio_secret_key: str = Field("minioadmin", env="MINIO_SECRET_KEY")
    minio_secure: bool = Field(False, env="MINIO_SECURE")
    minio_bucket: str = Field("aid-artifacts", env="MINIO_BUCKET")
    
    # Monitoring
    prometheus_gateway: Optional[str] = Field(None, env="PROMETHEUS_GATEWAY")
    grafana_url: Optional[str] = Field(None, env="GRAFANA_URL")
    loki_url: Optional[str] = Field(None, env="LOKI_URL")
    
    # Security
    secret_key: str = Field(..., env="SECRET_KEY")
    access_token_expire_minutes: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # CORS
    allowed_origins: str = Field("*", env="ALLOWED_ORIGINS")
    allowed_methods: str = Field("*", env="ALLOWED_METHODS")
    allowed_headers: str = Field("*", env="ALLOWED_HEADERS")
    
    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_format: str = Field("json", env="LOG_FORMAT")
    log_file: Optional[str] = Field(None, env="LOG_FILE")
    
    # Performance
    worker_concurrency: int = Field(4, env="WORKER_CONCURRENCY")
    max_request_size: int = Field(16 * 1024 * 1024, env="MAX_REQUEST_SIZE")  # 16MB
    
    # Features
    enable_metrics: bool = Field(True, env="ENABLE_METRICS")
    enable_tracing: bool = Field(False, env="ENABLE_TRACING")
    enable_caching: bool = Field(True, env="ENABLE_CACHING")
    enable_rate_limiting: bool = Field(True, env="ENABLE_RATE_LIMITING")
    
    @validator("environment")
    def validate_environment(cls, v):
        """Validate environment setting."""
        allowed = ["development", "testing", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of: {allowed}")
        return v
    
    @validator("log_level")
    def validate_log_level(cls, v):
        """Validate log level."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"Log level must be one of: {allowed}")
        return v.upper()
    
    @validator("llm_primary_provider")
    def validate_primary_provider(cls, v):
        """Validate primary LLM provider."""
        allowed = ["openai", "anthropic", "ollama"]
        if v not in allowed:
            raise ValueError(f"Primary provider must be one of: {allowed}")
        return v
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment == "production"
    
    @property
    def database_config(self) -> Dict[str, Any]:
        """Get database configuration."""
        return {
            "url": self.database_url,
            "pool_size": self.database_pool_size,
            "max_overflow": self.database_max_overflow,
            "echo": self.debug
        }
    
    @property
    def llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration."""
        providers = {}
        
        if self.openai_api_key:
            providers["openai"] = {
                "enabled": True,
                "api_key": self.openai_api_key,
                "model": "gpt-4",
                "primary": self.llm_primary_provider == "openai",
                "fallback": "openai" in self.llm_fallback_providers.split(",")
            }
        
        if self.anthropic_api_key:
            providers["anthropic"] = {
                "enabled": True,
                "api_key": self.anthropic_api_key,
                "model": "claude-3-sonnet-20240229",
                "primary": self.llm_primary_provider == "anthropic",
                "fallback": "anthropic" in self.llm_fallback_providers.split(",")
            }
        
        providers["ollama"] = {
            "enabled": True,
            "base_url": self.ollama_base_url,
            "model": "llama2",
            "primary": self.llm_primary_provider == "ollama",
            "fallback": "ollama" in self.llm_fallback_providers.split(",")
        }
        
        return {
            "providers": providers,
            "max_retries": self.llm_max_retries,
            "timeout": self.llm_timeout
        }
    
    @property
    def proxmox_config(self) -> Optional[Dict[str, Any]]:
        """Get Proxmox configuration."""
        if not all([self.proxmox_host, self.proxmox_user, self.proxmox_password]):
            return None
        
        return {
            "host": self.proxmox_host,
            "user": self.proxmox_user,
            "password": self.proxmox_password,
            "verify_ssl": self.proxmox_verify_ssl
        }
    
    @property
    def gitlab_config(self) -> Optional[Dict[str, Any]]:
        """Get GitLab configuration."""
        if not all([self.gitlab_url, self.gitlab_token]):
            return None
        
        return {
            "url": self.gitlab_url,
            "token": self.gitlab_token,
            "project_namespace": self.gitlab_project_namespace
        }
    
    @property
    def minio_config(self) -> Dict[str, Any]:
        """Get MinIO configuration."""
        return {
            "endpoint": self.minio_endpoint,
            "access_key": self.minio_access_key,
            "secret_key": self.minio_secret_key,
            "secure": self.minio_secure,
            "bucket": self.minio_bucket
        }
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()