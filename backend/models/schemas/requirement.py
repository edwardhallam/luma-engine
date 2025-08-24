"""Requirement analysis related Pydantic models."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class RequirementAnalysisRequest(BaseModel):
    """Request for requirement analysis."""

    user_request: str = Field(
        ..., min_length=10, description="Natural language requirement description"
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional context"
    )
    preferences: Optional[Dict[str, Any]] = Field(
        default=None, description="User preferences"
    )
    constraints: Optional[Dict[str, Any]] = Field(
        default=None, description="Resource or other constraints"
    )


class RequirementAnalysisResponse(BaseModel):
    """Response from requirement analysis."""

    success: bool = Field(..., description="Whether analysis was successful")
    specification: Optional[Dict[str, Any]] = Field(
        default=None, description="Generated deployment specification"
    )
    confidence_score: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Confidence in the analysis"
    )

    # Analysis metadata
    analysis_id: str = Field(..., description="Unique analysis identifier")
    created_at: datetime = Field(..., description="Analysis timestamp")
    provider_used: str = Field(..., description="LLM provider used")

    # Alternative suggestions
    alternatives: List[Dict[str, Any]] = Field(
        default_factory=list, description="Alternative specifications"
    )
    recommendations: List[str] = Field(
        default_factory=list, description="Additional recommendations"
    )

    # Warnings and notes
    warnings: List[str] = Field(
        default_factory=list, description="Potential issues or warnings"
    )
    assumptions: List[str] = Field(
        default_factory=list, description="Assumptions made during analysis"
    )

    # Error information
    error_message: Optional[str] = Field(
        default=None, description="Error message if analysis failed"
    )
    raw_response: Optional[str] = Field(
        default=None, description="Raw LLM response for debugging"
    )


class RequirementRefinementRequest(BaseModel):
    """Request to refine an existing requirement analysis."""

    analysis_id: str = Field(..., description="Original analysis identifier")
    feedback: str = Field(..., description="User feedback on the analysis")
    modifications: Optional[Dict[str, Any]] = Field(
        default=None, description="Specific modifications requested"
    )
    validation_errors: Optional[List[str]] = Field(
        default=None, description="Validation errors to address"
    )


class RequirementValidation(BaseModel):
    """Requirement validation result."""

    valid: bool = Field(..., description="Whether requirements are valid")
    errors: List[str] = Field(default_factory=list, description="Validation errors")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
    suggestions: List[str] = Field(
        default_factory=list, description="Improvement suggestions"
    )


class RequirementTemplate(BaseModel):
    """Template for common requirement patterns."""

    template_id: str = Field(..., description="Template identifier")
    name: str = Field(..., description="Template name")
    description: str = Field(..., description="Template description")
    category: str = Field(..., description="Template category")

    # Template content
    default_spec: Dict[str, Any] = Field(..., description="Default specification")
    required_fields: List[str] = Field(
        ..., description="Required fields for this template"
    )
    optional_fields: List[str] = Field(
        default_factory=list, description="Optional fields"
    )

    # Usage information
    use_cases: List[str] = Field(default_factory=list, description="Common use cases")
    examples: List[str] = Field(
        default_factory=list, description="Example requirements"
    )

    # Metadata
    created_by: str = Field(..., description="Template creator")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    usage_count: int = Field(default=0, description="Number of times used")


class RequirementHistory(BaseModel):
    """History of requirement analyses."""

    analysis_id: str = Field(..., description="Analysis identifier")
    original_request: str = Field(..., description="Original user request")
    final_specification: Dict[str, Any] = Field(
        ..., description="Final deployment specification"
    )

    # Analysis process
    iterations: List[Dict[str, Any]] = Field(
        default_factory=list, description="Analysis iterations"
    )
    feedback_provided: List[str] = Field(
        default_factory=list, description="User feedback given"
    )

    # Outcome
    deployed: bool = Field(
        default=False, description="Whether specification was deployed"
    )
    deployment_id: Optional[str] = Field(
        default=None, description="Resulting deployment ID"
    )
    success_rating: Optional[int] = Field(
        default=None, ge=1, le=5, description="User success rating"
    )

    # Metadata
    created_at: datetime = Field(..., description="Analysis start time")
    completed_at: Optional[datetime] = Field(
        default=None, description="Analysis completion time"
    )
    total_duration_seconds: Optional[int] = Field(
        default=None, description="Total analysis duration"
    )


class RequirementInsight(BaseModel):
    """Insights derived from requirement analysis patterns."""

    insight_type: str = Field(..., description="Type of insight")
    description: str = Field(..., description="Insight description")
    frequency: int = Field(..., description="Number of times this pattern was observed")
    success_rate: float = Field(
        ..., ge=0.0, le=1.0, description="Success rate for this pattern"
    )

    # Pattern details
    pattern_keywords: List[str] = Field(
        default_factory=list, description="Keywords associated with pattern"
    )
    common_specifications: Dict[str, Any] = Field(
        default_factory=dict, description="Common specification patterns"
    )

    # Recommendations
    optimization_suggestions: List[str] = Field(
        default_factory=list, description="Optimization suggestions"
    )
    pitfalls_to_avoid: List[str] = Field(
        default_factory=list, description="Common pitfalls"
    )

    # Metadata
    first_observed: datetime = Field(
        ..., description="First time this pattern was observed"
    )
    last_observed: datetime = Field(..., description="Most recent observation")
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence in this insight"
    )
