"""Template-related Pydantic models."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TemplateCategory(str, Enum):
    """Template categories."""

    CHAT_SERVICES = "chat-services"
    MCP_SERVERS = "mcp-servers"
    DATABASES = "databases"
    MODEL_SERVING = "model-serving"
    WEB_APPLICATIONS = "web-applications"
    MONITORING = "monitoring"
    NETWORKING = "networking"
    STORAGE = "storage"
    BASE = "base"


class TemplateStatus(str, Enum):
    """Template status values."""

    ACTIVE = "active"
    DEPRECATED = "deprecated"
    BETA = "beta"
    ARCHIVED = "archived"


class TemplateParameter(BaseModel):
    """Template parameter definition."""

    name: str = Field(..., description="Parameter name")
    type: str = Field(..., description="Parameter type (string, number, boolean, etc.)")
    description: str = Field(..., description="Parameter description")
    required: bool = Field(default=True, description="Whether parameter is required")
    default_value: Optional[Any] = Field(default=None, description="Default value")
    allowed_values: Optional[List[Any]] = Field(
        default=None, description="Allowed values (for enums)"
    )
    validation_pattern: Optional[str] = Field(
        default=None, description="Regex validation pattern"
    )
    min_value: Optional[float] = Field(
        default=None, description="Minimum value (for numbers)"
    )
    max_value: Optional[float] = Field(
        default=None, description="Maximum value (for numbers)"
    )


class TemplateResource(BaseModel):
    """Template resource definition."""

    type: str = Field(..., description="Resource type (vm, container, service, etc.)")
    name: str = Field(..., description="Resource name")
    configuration: Dict[str, Any] = Field(..., description="Resource configuration")
    dependencies: List[str] = Field(
        default_factory=list, description="Resource dependencies"
    )


class TemplateValidation(BaseModel):
    """Template validation rules."""

    pre_deployment: List[str] = Field(
        default_factory=list, description="Pre-deployment validation rules"
    )
    post_deployment: List[str] = Field(
        default_factory=list, description="Post-deployment validation rules"
    )
    health_checks: List[Dict[str, Any]] = Field(
        default_factory=list, description="Health check definitions"
    )


class Template(BaseModel):
    """Infrastructure template definition."""

    template_id: str = Field(..., description="Unique template identifier")
    name: str = Field(..., description="Template name")
    description: str = Field(..., description="Template description")
    category: TemplateCategory = Field(..., description="Template category")
    status: TemplateStatus = Field(
        default=TemplateStatus.ACTIVE, description="Template status"
    )

    # Template content
    parameters: List[TemplateParameter] = Field(..., description="Template parameters")
    resources: List[TemplateResource] = Field(..., description="Template resources")
    validation: TemplateValidation = Field(
        default_factory=TemplateValidation, description="Validation rules"
    )

    # Files and artifacts
    iac_template: str = Field(
        ..., description="Infrastructure as Code template content"
    )
    config_files: Dict[str, str] = Field(
        default_factory=dict, description="Configuration file templates"
    )
    scripts: Dict[str, str] = Field(
        default_factory=dict, description="Setup/deployment scripts"
    )

    # Documentation
    readme: Optional[str] = Field(default=None, description="Template documentation")
    examples: List[Dict[str, Any]] = Field(
        default_factory=list, description="Usage examples"
    )
    best_practices: List[str] = Field(
        default_factory=list, description="Best practices for this template"
    )

    # Resource requirements
    min_cpu: float = Field(default=0.5, description="Minimum CPU cores")
    min_memory_gb: float = Field(default=1.0, description="Minimum memory in GB")
    min_storage_gb: float = Field(default=10.0, description="Minimum storage in GB")
    supports_gpu: bool = Field(
        default=False, description="Whether template supports GPU"
    )

    # Platform support
    supported_platforms: List[str] = Field(
        default_factory=lambda: ["proxmox"], description="Supported platforms"
    )
    platform_specific_config: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict, description="Platform-specific configurations"
    )

    # Metadata
    version: str = Field(..., description="Template version")
    author: str = Field(..., description="Template author")
    organization: Optional[str] = Field(default=None, description="Author organization")
    license: str = Field(default="MIT", description="Template license")
    tags: List[str] = Field(default_factory=list, description="Template tags")

    # Usage statistics
    usage_count: int = Field(default=0, description="Number of times used")
    success_rate: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Deployment success rate"
    )
    average_deploy_time: Optional[int] = Field(
        default=None, description="Average deployment time in seconds"
    )

    # Timestamps
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    last_used: Optional[datetime] = Field(
        default=None, description="Last usage timestamp"
    )


class TemplateRequest(BaseModel):
    """Request to create or update a template."""

    name: str = Field(..., min_length=1, max_length=100, description="Template name")
    description: str = Field(..., min_length=10, description="Template description")
    category: TemplateCategory = Field(..., description="Template category")

    # Template content
    parameters: List[TemplateParameter] = Field(..., description="Template parameters")
    iac_template: str = Field(..., description="Infrastructure as Code template")
    config_files: Optional[Dict[str, str]] = Field(
        default=None, description="Configuration files"
    )
    scripts: Optional[Dict[str, str]] = Field(default=None, description="Setup scripts")

    # Documentation
    readme: Optional[str] = Field(default=None, description="Template documentation")
    examples: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Usage examples"
    )

    # Metadata
    version: str = Field(default="1.0.0", description="Template version")
    tags: Optional[List[str]] = Field(default=None, description="Template tags")
    supported_platforms: Optional[List[str]] = Field(
        default=None, description="Supported platforms"
    )


class TemplateResponse(BaseModel):
    """Response for template operations."""

    template: Template = Field(..., description="Template data")
    validation_result: Optional[Dict[str, Any]] = Field(
        default=None, description="Template validation result"
    )
    deployment_preview: Optional[Dict[str, Any]] = Field(
        default=None, description="Preview of what would be deployed"
    )


class TemplateListResponse(BaseModel):
    """Response for listing templates."""

    templates: List[Template] = Field(..., description="List of templates")
    total: int = Field(..., description="Total number of templates")
    categories: List[str] = Field(..., description="Available categories")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")


class TemplateValidationRequest(BaseModel):
    """Request to validate a template."""

    template: Template = Field(..., description="Template to validate")
    target_platform: str = Field(
        default="proxmox", description="Target platform for validation"
    )
    parameter_values: Optional[Dict[str, Any]] = Field(
        default=None, description="Parameter values for testing"
    )


class TemplateValidationResponse(BaseModel):
    """Response from template validation."""

    valid: bool = Field(..., description="Whether template is valid")
    errors: List[str] = Field(default_factory=list, description="Validation errors")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
    suggestions: List[str] = Field(
        default_factory=list, description="Improvement suggestions"
    )

    # Detailed validation results
    syntax_valid: bool = Field(..., description="Whether syntax is valid")
    parameters_valid: bool = Field(..., description="Whether parameters are valid")
    resources_valid: bool = Field(..., description="Whether resources are valid")
    dependencies_valid: bool = Field(..., description="Whether dependencies are valid")

    # Generated preview
    generated_iac: Optional[str] = Field(
        default=None, description="Generated IaC for preview"
    )
    estimated_cost: Optional[float] = Field(
        default=None, description="Estimated monthly cost"
    )


class TemplateUsageStats(BaseModel):
    """Template usage statistics."""

    template_id: str = Field(..., description="Template identifier")
    total_deployments: int = Field(..., description="Total number of deployments")
    successful_deployments: int = Field(
        ..., description="Number of successful deployments"
    )
    failed_deployments: int = Field(..., description="Number of failed deployments")

    # Performance metrics
    average_deploy_time: float = Field(
        ..., description="Average deployment time in seconds"
    )
    median_deploy_time: float = Field(
        ..., description="Median deployment time in seconds"
    )
    fastest_deploy_time: float = Field(
        ..., description="Fastest deployment time in seconds"
    )
    slowest_deploy_time: float = Field(
        ..., description="Slowest deployment time in seconds"
    )

    # Usage patterns
    most_common_parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Most commonly used parameter values"
    )
    platform_usage: Dict[str, int] = Field(
        default_factory=dict, description="Usage by platform"
    )
    monthly_usage: Dict[str, int] = Field(
        default_factory=dict, description="Usage by month"
    )

    # Timestamps
    first_used: datetime = Field(..., description="First usage timestamp")
    last_used: datetime = Field(..., description="Last usage timestamp")
    stats_generated: datetime = Field(
        ..., description="When these stats were generated"
    )
