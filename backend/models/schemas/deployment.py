"""Deployment-related Pydantic models."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ServiceType(str, Enum):
    """Supported service types."""

    CHAT_SERVICE = "chat-service"
    MCP_SERVER = "mcp-server"
    DATABASE = "database"
    MODEL_SERVING = "model-serving"
    WEB_APPLICATION = "web-application"
    API_SERVICE = "api-service"
    MONITORING = "monitoring"
    STORAGE = "storage"


class DeploymentStatus(str, Enum):
    """Deployment status values."""

    PENDING = "pending"
    ANALYZING = "analyzing"
    GENERATING = "generating"
    DEPLOYING = "deploying"
    RUNNING = "running"
    FAILED = "failed"
    STOPPED = "stopped"
    UPDATING = "updating"


class ResourceRequirements(BaseModel):
    """Resource requirements specification."""

    cpu_cores: float = Field(..., ge=0.1, description="CPU cores required")
    memory_gb: float = Field(..., ge=0.1, description="RAM in GB")
    storage_gb: float = Field(..., ge=1, description="Storage in GB")
    gpu_required: bool = Field(default=False, description="Whether GPU is needed")
    gpu_memory_gb: Optional[float] = Field(
        default=None, ge=1, description="GPU memory in GB"
    )


class ScalingConfig(BaseModel):
    """Auto-scaling configuration."""

    min_instances: int = Field(default=1, ge=1, description="Minimum instances")
    max_instances: int = Field(default=1, ge=1, description="Maximum instances")
    auto_scaling: bool = Field(default=False, description="Enable auto-scaling")
    cpu_threshold: Optional[float] = Field(
        default=80.0, ge=1, le=100, description="CPU threshold for scaling"
    )
    memory_threshold: Optional[float] = Field(
        default=80.0, ge=1, le=100, description="Memory threshold for scaling"
    )


class NetworkingConfig(BaseModel):
    """Networking configuration."""

    external_access: bool = Field(default=False, description="Needs internet access")
    load_balancer: bool = Field(default=False, description="Needs load balancing")
    ssl_required: bool = Field(default=True, description="Requires SSL/TLS")
    custom_domain: Optional[str] = Field(default=None, description="Custom domain name")
    ports: List[int] = Field(default_factory=list, description="Exposed ports")


class MonitoringConfig(BaseModel):
    """Monitoring configuration."""

    metrics_enabled: bool = Field(default=True, description="Enable metrics collection")
    logging_level: str = Field(default="INFO", description="Logging level")
    health_check_path: str = Field(
        default="/health", description="Health check endpoint"
    )
    alerts_enabled: bool = Field(default=True, description="Enable alerting")


class BackupConfig(BaseModel):
    """Backup configuration."""

    enabled: bool = Field(default=True, description="Enable backups")
    frequency: str = Field(default="daily", description="Backup frequency")
    retention_days: int = Field(default=30, ge=1, description="Backup retention period")
    storage_location: Optional[str] = Field(
        default=None, description="Backup storage location"
    )


class ServiceDependency(BaseModel):
    """Service dependency specification."""

    service: str = Field(..., description="Dependency service name")
    type: str = Field(..., description="Dependency type")
    required: bool = Field(default=True, description="Whether dependency is required")
    version: Optional[str] = Field(default=None, description="Required version")


class DeploymentSpec(BaseModel):
    """Complete deployment specification."""

    service_type: ServiceType = Field(..., description="Type of service to deploy")
    service_name: str = Field(
        ..., min_length=1, max_length=63, description="Unique service name"
    )
    description: str = Field(..., description="Service description")
    template: str = Field(..., description="Template to use for deployment")

    resource_requirements: ResourceRequirements
    configuration: Dict[str, Any] = Field(
        default_factory=dict, description="Service configuration"
    )
    dependencies: List[ServiceDependency] = Field(
        default_factory=list, description="Service dependencies"
    )
    scaling: ScalingConfig = Field(
        default_factory=ScalingConfig, description="Scaling configuration"
    )
    networking: NetworkingConfig = Field(
        default_factory=NetworkingConfig, description="Networking configuration"
    )
    monitoring: MonitoringConfig = Field(
        default_factory=MonitoringConfig, description="Monitoring configuration"
    )
    backup: BackupConfig = Field(
        default_factory=BackupConfig, description="Backup configuration"
    )


class DeploymentRequest(BaseModel):
    """Request to create a new deployment."""

    user_request: str = Field(
        ..., min_length=10, description="Natural language deployment request"
    )
    target_platform: str = Field(
        default="proxmox", description="Target deployment platform"
    )
    resource_constraints: Optional[Dict[str, Any]] = Field(
        default=None, description="Resource constraints"
    )
    override_spec: Optional[DeploymentSpec] = Field(
        default=None, description="Override auto-generated spec"
    )


class IaCFile(BaseModel):
    """Generated Infrastructure as Code file."""

    filename: str = Field(..., description="File name")
    content: str = Field(..., description="File content")
    file_type: str = Field(
        ..., description="File type (main, variables, outputs, etc.)"
    )


class DeploymentResponse(BaseModel):
    """Response for deployment operations."""

    deployment_id: str = Field(..., description="Unique deployment identifier")
    status: DeploymentStatus = Field(..., description="Current deployment status")
    specification: Optional[DeploymentSpec] = Field(
        default=None, description="Deployment specification"
    )
    iac_files: List[IaCFile] = Field(
        default_factory=list, description="Generated IaC files"
    )

    # Status information
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    progress: int = Field(
        default=0, ge=0, le=100, description="Deployment progress percentage"
    )

    # Error information
    error_message: Optional[str] = Field(
        default=None, description="Error message if failed"
    )
    validation_errors: List[str] = Field(
        default_factory=list, description="Validation errors"
    )

    # Resource information
    allocated_resources: Optional[ResourceRequirements] = Field(
        default=None, description="Actually allocated resources"
    )
    cost_estimate: Optional[float] = Field(
        default=None, description="Monthly cost estimate"
    )

    # URLs and endpoints
    endpoints: Dict[str, str] = Field(
        default_factory=dict, description="Service endpoints"
    )
    management_urls: Dict[str, str] = Field(
        default_factory=dict, description="Management interface URLs"
    )


class DeploymentUpdateRequest(BaseModel):
    """Request to update an existing deployment."""

    specification: Optional[DeploymentSpec] = Field(
        default=None, description="Updated specification"
    )
    action: str = Field(..., description="Update action (update, restart, stop, start)")
    force: bool = Field(default=False, description="Force update even if risky")


class DeploymentListResponse(BaseModel):
    """Response for listing deployments."""

    deployments: List[DeploymentResponse] = Field(
        ..., description="List of deployments"
    )
    total: int = Field(..., description="Total number of deployments")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")


class DeploymentMetrics(BaseModel):
    """Deployment metrics and status."""

    deployment_id: str = Field(..., description="Deployment identifier")
    cpu_usage: float = Field(..., description="CPU usage percentage")
    memory_usage: float = Field(..., description="Memory usage percentage")
    storage_usage: float = Field(..., description="Storage usage percentage")
    network_in: float = Field(..., description="Network input in MB/s")
    network_out: float = Field(..., description="Network output in MB/s")
    uptime_seconds: int = Field(..., description="Uptime in seconds")
    health_status: str = Field(..., description="Overall health status")
    last_updated: datetime = Field(..., description="Last metrics update")


class DeploymentLogs(BaseModel):
    """Deployment logs."""

    deployment_id: str = Field(..., description="Deployment identifier")
    logs: List[str] = Field(..., description="Log entries")
    log_level: str = Field(default="INFO", description="Log level filter")
    start_time: Optional[datetime] = Field(
        default=None, description="Start time for log range"
    )
    end_time: Optional[datetime] = Field(
        default=None, description="End time for log range"
    )
