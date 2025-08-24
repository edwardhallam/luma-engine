"""Infrastructure as Code generation schemas."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class IaCProvider(str, Enum):
    """Supported IaC providers."""

    PROXMOX = "proxmox"
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    DIGITALOCEAN = "digitalocean"
    LINODE = "linode"
    HETZNER = "hetzner"
    VULTR = "vultr"


class IaCFormat(str, Enum):
    """Supported IaC formats."""

    TERRAFORM = "terraform"
    OPENTOFU = "opentofu"
    PULUMI = "pulumi"
    CDK = "cdk"


class ValidationSeverity(str, Enum):
    """Validation issue severity levels."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class IaCGenerationRequest(BaseModel):
    """Request for IaC generation."""

    # Template and requirements
    template_id: Optional[str] = Field(default=None, description="Template ID to use")
    requirements: str = Field(..., description="Natural language requirements")

    # Target configuration
    provider: IaCProvider = Field(..., description="Target infrastructure provider")
    format: IaCFormat = Field(default=IaCFormat.TERRAFORM, description="IaC format")

    # Generation options
    enable_validation: bool = Field(
        default=True, description="Enable syntax validation"
    )
    enable_optimization: bool = Field(
        default=True, description="Enable cost optimization"
    )
    include_best_practices: bool = Field(
        default=True, description="Apply best practices"
    )

    # Parameter overrides
    parameter_values: Optional[Dict[str, Any]] = Field(
        default=None, description="Parameter value overrides"
    )

    # Generation context
    project_name: str = Field(..., description="Project name for resource naming")
    environment: str = Field(default="development", description="Target environment")
    tags: Optional[Dict[str, str]] = Field(
        default=None, description="Default resource tags"
    )


class ValidationIssue(BaseModel):
    """IaC validation issue."""

    severity: ValidationSeverity = Field(..., description="Issue severity")
    message: str = Field(..., description="Issue description")
    line: Optional[int] = Field(default=None, description="Line number (if applicable)")
    column: Optional[int] = Field(
        default=None, description="Column number (if applicable)"
    )
    rule: Optional[str] = Field(
        default=None, description="Validation rule that triggered"
    )
    suggestion: Optional[str] = Field(default=None, description="Suggested fix")


class IaCValidationResult(BaseModel):
    """IaC validation result."""

    valid: bool = Field(..., description="Whether IaC is valid")
    syntax_valid: bool = Field(..., description="Whether syntax is valid")
    security_valid: bool = Field(..., description="Whether security checks pass")

    # Issues found
    errors: List[ValidationIssue] = Field(
        default_factory=list, description="Error issues"
    )
    warnings: List[ValidationIssue] = Field(
        default_factory=list, description="Warning issues"
    )
    info: List[ValidationIssue] = Field(default_factory=list, description="Info issues")

    # Statistics
    total_issues: int = Field(..., description="Total number of issues")
    error_count: int = Field(..., description="Number of errors")
    warning_count: int = Field(..., description="Number of warnings")

    # Tool outputs
    terraform_plan: Optional[str] = Field(
        default=None, description="Terraform plan output"
    )
    security_scan_results: Optional[Dict[str, Any]] = Field(
        default=None, description="Security scan results"
    )


class CostEstimate(BaseModel):
    """Infrastructure cost estimate."""

    # Total costs
    monthly_cost: float = Field(..., description="Estimated monthly cost in USD")
    annual_cost: float = Field(..., description="Estimated annual cost in USD")

    # Cost breakdown
    compute_cost: float = Field(..., description="Compute resources cost")
    storage_cost: float = Field(..., description="Storage cost")
    network_cost: float = Field(..., description="Network/bandwidth cost")
    other_cost: float = Field(..., description="Other services cost")

    # Resource breakdown
    resource_costs: Dict[str, float] = Field(
        default_factory=dict, description="Cost by resource"
    )

    # Optimization suggestions
    optimization_opportunities: List[str] = Field(
        default_factory=list, description="Cost optimization opportunities"
    )
    potential_savings: float = Field(
        default=0.0, description="Potential monthly savings from optimizations"
    )


class GeneratedResource(BaseModel):
    """Generated infrastructure resource."""

    name: str = Field(..., description="Resource name")
    type: str = Field(..., description="Resource type")
    provider: IaCProvider = Field(..., description="Provider")
    configuration: Dict[str, Any] = Field(..., description="Resource configuration")
    dependencies: List[str] = Field(default_factory=list, description="Dependencies")

    # Cost information
    estimated_monthly_cost: Optional[float] = Field(
        default=None, description="Estimated monthly cost"
    )


class IaCGenerationResult(BaseModel):
    """Result of IaC generation."""

    # Generation metadata
    generation_id: str = Field(..., description="Unique generation ID")
    provider: IaCProvider = Field(..., description="Target provider")
    format: IaCFormat = Field(..., description="Generated format")

    # Generated content
    iac_code: str = Field(..., description="Generated IaC code")
    configuration_files: Dict[str, str] = Field(
        default_factory=dict, description="Additional configuration files"
    )
    scripts: Dict[str, str] = Field(
        default_factory=dict, description="Setup/deployment scripts"
    )

    # Resource information
    resources: List[GeneratedResource] = Field(
        default_factory=list, description="Generated resources"
    )

    # Validation results
    validation_result: IaCValidationResult = Field(
        ..., description="Validation results"
    )

    # Cost analysis
    cost_estimate: Optional[CostEstimate] = Field(
        default=None, description="Cost estimate"
    )

    # Documentation
    readme: str = Field(..., description="Generated documentation")
    deployment_instructions: str = Field(..., description="Deployment instructions")

    # Metadata
    template_used: Optional[str] = Field(default=None, description="Template ID used")
    requirements_analyzed: str = Field(..., description="Original requirements")
    generation_time: float = Field(..., description="Generation time in seconds")
    created_at: datetime = Field(..., description="Generation timestamp")


class IaCGenerationResponse(BaseModel):
    """Response for IaC generation."""

    success: bool = Field(..., description="Whether generation was successful")
    result: Optional[IaCGenerationResult] = Field(
        default=None, description="Generation result (if successful)"
    )

    # Error information
    error: Optional[str] = Field(default=None, description="Error message (if failed)")
    error_details: Optional[Dict[str, Any]] = Field(
        default=None, description="Detailed error information"
    )

    # Processing information
    processing_time: float = Field(..., description="Total processing time in seconds")
    llm_calls: int = Field(..., description="Number of LLM API calls made")
    tokens_used: Optional[int] = Field(default=None, description="Total tokens used")


class IaCValidationRequest(BaseModel):
    """Request for IaC validation."""

    iac_code: str = Field(..., description="IaC code to validate")
    format: IaCFormat = Field(..., description="IaC format")
    provider: IaCProvider = Field(..., description="Target provider")

    # Validation options
    check_syntax: bool = Field(default=True, description="Enable syntax validation")
    check_security: bool = Field(default=True, description="Enable security validation")
    check_best_practices: bool = Field(default=True, description="Check best practices")
    check_costs: bool = Field(default=False, description="Enable cost analysis")

    # Context for validation
    project_name: Optional[str] = Field(default=None, description="Project name")
    environment: Optional[str] = Field(default=None, description="Target environment")


class IaCValidationResponse(BaseModel):
    """Response for IaC validation."""

    validation_result: IaCValidationResult = Field(
        ..., description="Validation results"
    )
    cost_estimate: Optional[CostEstimate] = Field(
        default=None, description="Cost estimate (if requested)"
    )

    # Processing information
    processing_time: float = Field(..., description="Validation time in seconds")
