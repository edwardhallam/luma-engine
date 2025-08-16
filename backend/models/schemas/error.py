"""Error diagnosis related Pydantic models."""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class ErrorCategory(str, Enum):
    """Error categories."""
    INFRASTRUCTURE = "infrastructure"
    CONFIGURATION = "configuration"
    DEPENDENCY = "dependency"
    RESOURCE = "resource"
    SECURITY = "security"
    NETWORK = "network"
    APPLICATION = "application"
    UNKNOWN = "unknown"


class ErrorSeverity(str, Enum):
    """Error severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RiskLevel(str, Enum):
    """Risk levels for actions."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ErrorAnalysis(BaseModel):
    """Error analysis details."""
    category: ErrorCategory = Field(..., description="Error category")
    severity: ErrorSeverity = Field(..., description="Error severity")
    root_cause: str = Field(..., description="Root cause description")
    affected_components: List[str] = Field(..., description="Affected components")
    error_pattern: str = Field(..., description="Error pattern for learning")


class ImmediateAction(BaseModel):
    """Immediate action to take."""
    action: str = Field(..., description="Action description")
    command: Optional[str] = Field(default=None, description="Command to execute")
    reason: str = Field(..., description="Reason for this action")
    risk_level: RiskLevel = Field(..., description="Risk level of action")
    estimated_time: Optional[int] = Field(default=None, description="Estimated time in seconds")


class RootCauseFix(BaseModel):
    """Root cause fix."""
    fix: str = Field(..., description="Fix description")
    implementation: str = Field(..., description="Implementation details")
    prevention: str = Field(..., description="Prevention strategy")
    testing: str = Field(..., description="Testing strategy")
    rollback_plan: Optional[str] = Field(default=None, description="Rollback plan")


class MonitoringRecommendation(BaseModel):
    """Monitoring recommendation."""
    metric: str = Field(..., description="Metric to monitor")
    threshold: str = Field(..., description="Alert threshold")
    action: str = Field(..., description="Action when threshold exceeded")
    priority: int = Field(default=1, ge=1, le=5, description="Priority level")


class ErrorDiagnosisRequest(BaseModel):
    """Request for error diagnosis."""
    error_logs: str = Field(..., description="Error logs or messages")
    deployment_config: Dict[str, Any] = Field(..., description="Deployment configuration")
    system_state: Dict[str, Any] = Field(..., description="Current system state")
    previous_fixes: Optional[List[str]] = Field(default=None, description="Previously attempted fixes")
    
    # Context information
    deployment_id: Optional[str] = Field(default=None, description="Related deployment ID")
    service_name: Optional[str] = Field(default=None, description="Affected service name")
    platform: str = Field(default="proxmox", description="Target platform")
    
    # Timing information
    error_started: Optional[datetime] = Field(default=None, description="When error first occurred")
    last_working: Optional[datetime] = Field(default=None, description="Last known working state")


class ErrorDiagnosisResponse(BaseModel):
    """Response from error diagnosis."""
    success: bool = Field(..., description="Whether diagnosis was successful")
    diagnosis_id: str = Field(..., description="Unique diagnosis identifier")
    
    # Analysis results
    error_analysis: Optional[ErrorAnalysis] = Field(default=None, description="Error analysis")
    immediate_actions: List[ImmediateAction] = Field(default_factory=list, description="Immediate actions")
    root_cause_fixes: List[RootCauseFix] = Field(default_factory=list, description="Root cause fixes")
    monitoring_recommendations: List[MonitoringRecommendation] = Field(default_factory=list, description="Monitoring recommendations")
    
    # Metadata
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence in diagnosis")
    estimated_resolution_time: Optional[str] = Field(default=None, description="Estimated resolution time")
    requires_manual_intervention: bool = Field(default=False, description="Requires manual intervention")
    
    # Provider information
    provider_used: str = Field(..., description="LLM provider used")
    created_at: datetime = Field(..., description="Diagnosis timestamp")
    
    # Error information
    error_message: Optional[str] = Field(default=None, description="Error message if diagnosis failed")
    raw_response: Optional[str] = Field(default=None, description="Raw LLM response")


class ErrorResolutionRequest(BaseModel):
    """Request to execute error resolution."""
    diagnosis_id: str = Field(..., description="Diagnosis identifier")
    selected_actions: List[int] = Field(..., description="Indices of selected actions to execute")
    force_execution: bool = Field(default=False, description="Force execution even if risky")
    dry_run: bool = Field(default=False, description="Only simulate the actions")


class ErrorResolutionResponse(BaseModel):
    """Response from error resolution execution."""
    success: bool = Field(..., description="Whether resolution was successful")
    resolution_id: str = Field(..., description="Unique resolution identifier")
    
    # Execution results
    executed_actions: List[Dict[str, Any]] = Field(..., description="Actions that were executed")
    failed_actions: List[Dict[str, Any]] = Field(default_factory=list, description="Actions that failed")
    
    # Status
    resolution_status: str = Field(..., description="Resolution status")
    error_resolved: bool = Field(default=False, description="Whether error was resolved")
    
    # Metadata
    started_at: datetime = Field(..., description="Resolution start time")
    completed_at: Optional[datetime] = Field(default=None, description="Resolution completion time")
    total_duration: Optional[int] = Field(default=None, description="Total duration in seconds")


class ErrorPattern(BaseModel):
    """Error pattern for learning."""
    pattern_id: str = Field(..., description="Unique pattern identifier")
    pattern_name: str = Field(..., description="Pattern name")
    category: ErrorCategory = Field(..., description="Error category")
    
    # Pattern definition
    triggers: List[str] = Field(..., description="Conditions that trigger this error")
    symptoms: List[str] = Field(..., description="Observable symptoms")
    common_causes: List[str] = Field(..., description="Common root causes")
    
    # Resolution information
    resolution_steps: List[Dict[str, Any]] = Field(..., description="Resolution steps")
    prevention_measures: List[str] = Field(..., description="Prevention measures")
    automation_potential: str = Field(..., description="Automation potential")
    
    # Learning metadata
    occurrence_count: int = Field(default=1, description="Number of times observed")
    success_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Resolution success rate")
    confidence_level: float = Field(default=0.0, ge=0.0, le=1.0, description="Pattern confidence")
    
    # Related patterns
    related_patterns: List[str] = Field(default_factory=list, description="Related pattern IDs")
    parent_pattern: Optional[str] = Field(default=None, description="Parent pattern ID")
    child_patterns: List[str] = Field(default_factory=list, description="Child pattern IDs")
    
    # Timestamps
    first_observed: datetime = Field(..., description="First observation")
    last_observed: datetime = Field(..., description="Last observation")
    created_at: datetime = Field(..., description="Pattern creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class ErrorKnowledgeBase(BaseModel):
    """Error knowledge base entry."""
    kb_id: str = Field(..., description="Knowledge base entry ID")
    title: str = Field(..., description="Entry title")
    description: str = Field(..., description="Entry description")
    
    # Content
    error_patterns: List[ErrorPattern] = Field(..., description="Associated error patterns")
    solutions: List[Dict[str, Any]] = Field(..., description="Known solutions")
    documentation_links: List[str] = Field(default_factory=list, description="Related documentation")
    
    # Metadata
    created_by: str = Field(..., description="Creator")
    verified: bool = Field(default=False, description="Whether entry is verified")
    rating: float = Field(default=0.0, ge=0.0, le=5.0, description="Community rating")
    usage_count: int = Field(default=0, description="Number of times used")
    
    # Timestamps
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    last_used: Optional[datetime] = Field(default=None, description="Last usage timestamp")


class ErrorInsight(BaseModel):
    """Insights derived from error analysis."""
    insight_id: str = Field(..., description="Insight identifier")
    insight_type: str = Field(..., description="Type of insight")
    description: str = Field(..., description="Insight description")
    
    # Data
    frequency: int = Field(..., description="Frequency of occurrence")
    trend: str = Field(..., description="Trend over time")
    impact_assessment: str = Field(..., description="Impact assessment")
    
    # Recommendations
    preventive_actions: List[str] = Field(default_factory=list, description="Preventive actions")
    process_improvements: List[str] = Field(default_factory=list, description="Process improvements")
    tool_recommendations: List[str] = Field(default_factory=list, description="Tool recommendations")
    
    # Metadata
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in insight")
    data_period: str = Field(..., description="Data period analyzed")
    generated_at: datetime = Field(..., description="Insight generation timestamp")