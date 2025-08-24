"""LLM service related Pydantic models."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class LLMProviderStatus(BaseModel):
    """Status of an LLM provider."""

    provider_name: str = Field(..., description="Provider name")
    available: bool = Field(..., description="Whether provider is available")
    primary: bool = Field(
        default=False, description="Whether this is the primary provider"
    )
    fallback: bool = Field(
        default=False, description="Whether this is a fallback provider"
    )

    # Configuration (without sensitive data)
    model: Optional[str] = Field(default=None, description="Model being used")
    endpoint: Optional[str] = Field(default=None, description="Provider endpoint")

    # Status information
    last_check: datetime = Field(..., description="Last status check timestamp")
    response_time_ms: Optional[float] = Field(
        default=None, description="Last response time in milliseconds"
    )
    error_message: Optional[str] = Field(
        default=None, description="Error message if unavailable"
    )

    # Usage statistics
    requests_today: int = Field(default=0, description="Requests made today")
    tokens_used_today: int = Field(default=0, description="Tokens used today")
    success_rate: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Success rate over last 24h"
    )


class LLMRequest(BaseModel):
    """Generic LLM request."""

    operation: str = Field(..., description="LLM operation to perform")
    parameters: Dict[str, Any] = Field(..., description="Operation parameters")
    provider: Optional[str] = Field(
        default=None, description="Specific provider to use"
    )

    # Request options
    max_tokens: Optional[int] = Field(
        default=None, ge=1, le=8000, description="Maximum tokens to generate"
    )
    temperature: Optional[float] = Field(
        default=None, ge=0.0, le=2.0, description="Generation temperature"
    )
    stream: bool = Field(default=False, description="Whether to stream the response")

    # Context
    context: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional context"
    )
    session_id: Optional[str] = Field(
        default=None, description="Session identifier for continuity"
    )


class LLMResponse(BaseModel):
    """Generic LLM response."""

    success: bool = Field(..., description="Whether request was successful")
    result: Optional[Dict[str, Any]] = Field(
        default=None, description="Operation result"
    )

    # Response metadata
    request_id: str = Field(..., description="Unique request identifier")
    provider_used: str = Field(..., description="Provider that handled the request")
    model_used: str = Field(..., description="Model that generated the response")

    # Performance metrics
    response_time_ms: float = Field(..., description="Response time in milliseconds")
    tokens_used: int = Field(default=0, description="Tokens consumed")
    tokens_generated: int = Field(default=0, description="Tokens generated")

    # Error information
    error_message: Optional[str] = Field(
        default=None, description="Error message if failed"
    )
    error_code: Optional[str] = Field(default=None, description="Error code")
    retry_after: Optional[int] = Field(default=None, description="Retry after seconds")

    # Timestamps
    created_at: datetime = Field(..., description="Response timestamp")


class LLMUsageStats(BaseModel):
    """LLM usage statistics."""

    provider: str = Field(..., description="Provider name")
    time_period: str = Field(..., description="Time period for stats")

    # Request statistics
    total_requests: int = Field(..., description="Total number of requests")
    successful_requests: int = Field(..., description="Number of successful requests")
    failed_requests: int = Field(..., description="Number of failed requests")

    # Token usage
    total_tokens: int = Field(..., description="Total tokens used")
    input_tokens: int = Field(..., description="Input tokens")
    output_tokens: int = Field(..., description="Output tokens")

    # Performance metrics
    average_response_time: float = Field(
        ..., description="Average response time in milliseconds"
    )
    median_response_time: float = Field(
        ..., description="Median response time in milliseconds"
    )
    p95_response_time: float = Field(..., description="95th percentile response time")

    # Cost information
    estimated_cost: Optional[float] = Field(
        default=None, description="Estimated cost in USD"
    )
    cost_per_request: Optional[float] = Field(
        default=None, description="Average cost per request"
    )

    # Operation breakdown
    operations: Dict[str, int] = Field(
        default_factory=dict, description="Requests by operation type"
    )
    models_used: Dict[str, int] = Field(
        default_factory=dict, description="Requests by model"
    )

    # Error analysis
    error_types: Dict[str, int] = Field(
        default_factory=dict, description="Errors by type"
    )
    retry_count: int = Field(default=0, description="Number of retries performed")

    # Timestamps
    period_start: datetime = Field(..., description="Statistics period start")
    period_end: datetime = Field(..., description="Statistics period end")
    generated_at: datetime = Field(..., description="When statistics were generated")


class LLMConfiguration(BaseModel):
    """LLM service configuration."""

    providers: Dict[str, Dict[str, Any]] = Field(
        ..., description="Provider configurations"
    )
    default_provider: str = Field(..., description="Default provider name")
    fallback_providers: List[str] = Field(
        default_factory=list, description="Fallback provider names"
    )

    # Global settings
    max_retries: int = Field(
        default=3, ge=0, le=10, description="Maximum retry attempts"
    )
    timeout_seconds: int = Field(
        default=30, ge=1, le=300, description="Request timeout"
    )
    rate_limit_requests: int = Field(
        default=100, ge=1, description="Rate limit requests per minute"
    )

    # Caching
    cache_enabled: bool = Field(default=True, description="Enable response caching")
    cache_ttl_seconds: int = Field(
        default=3600, ge=0, description="Cache TTL in seconds"
    )

    # Monitoring
    metrics_enabled: bool = Field(default=True, description="Enable metrics collection")
    logging_level: str = Field(default="INFO", description="Logging level")

    # Security
    api_key_rotation: bool = Field(default=False, description="Enable API key rotation")
    request_sanitization: bool = Field(
        default=True, description="Enable request sanitization"
    )


class LLMHealthCheck(BaseModel):
    """LLM service health check result."""

    overall_status: str = Field(..., description="Overall health status")
    timestamp: datetime = Field(..., description="Health check timestamp")

    # Provider health
    providers: Dict[str, Dict[str, Any]] = Field(
        ..., description="Provider health status"
    )
    primary_provider_healthy: bool = Field(
        ..., description="Whether primary provider is healthy"
    )
    fallback_available: bool = Field(
        ..., description="Whether fallback providers are available"
    )

    # Performance metrics
    average_response_time: float = Field(
        ..., description="Recent average response time"
    )
    success_rate: float = Field(..., ge=0.0, le=1.0, description="Recent success rate")
    error_rate: float = Field(..., ge=0.0, le=1.0, description="Recent error rate")

    # Resource usage
    requests_per_minute: float = Field(..., description="Current requests per minute")
    tokens_per_minute: float = Field(..., description="Current tokens per minute")

    # Issues and recommendations
    issues: List[str] = Field(default_factory=list, description="Current issues")
    recommendations: List[str] = Field(
        default_factory=list, description="Health recommendations"
    )

    # Next check
    next_check_at: datetime = Field(..., description="Next scheduled health check")


class LLMPromptTemplate(BaseModel):
    """LLM prompt template definition."""

    template_id: str = Field(..., description="Template identifier")
    name: str = Field(..., description="Template name")
    description: str = Field(..., description="Template description")
    category: str = Field(..., description="Template category")

    # Template content
    prompt_template: str = Field(..., description="Prompt template with variables")
    input_variables: List[str] = Field(..., description="Required input variables")
    optional_variables: List[str] = Field(
        default_factory=list, description="Optional input variables"
    )

    # Configuration
    default_parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Default parameters"
    )
    recommended_models: List[str] = Field(
        default_factory=list, description="Recommended models"
    )

    # Usage information
    use_cases: List[str] = Field(default_factory=list, description="Common use cases")
    examples: List[Dict[str, Any]] = Field(
        default_factory=list, description="Usage examples"
    )

    # Metadata
    version: str = Field(..., description="Template version")
    created_by: str = Field(..., description="Template creator")
    usage_count: int = Field(default=0, description="Number of times used")

    # Performance
    average_tokens: int = Field(default=0, description="Average tokens in responses")
    success_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Success rate")

    # Timestamps
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    last_used: Optional[datetime] = Field(
        default=None, description="Last usage timestamp"
    )
