"""LLM service API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, status
from fastapi.responses import StreamingResponse

from backend.models.schemas import (
    LLMRequest,
    LLMResponse,
    LLMProviderStatus,
    LLMUsageStats,
    LLMConfiguration,
    LLMHealthCheck,
    LLMPromptTemplate,
    ErrorDiagnosisRequest,
    ErrorDiagnosisResponse,
)
from backend.core.exceptions import AIDException
from backend.llm.service import LLMService
import logging
import json

logger = logging.getLogger(__name__)
router = APIRouter()


def get_llm_service() -> LLMService:
    """Dependency to get LLM service instance."""
    # This will be implemented when we create the service layer
    raise NotImplementedError("LLMService dependency not yet implemented")


@router.post(
    "/analyze-requirements",
    response_model=LLMResponse,
    summary="Analyze requirements with LLM",
    description="Use LLM to analyze natural language requirements."
)
async def analyze_requirements_llm(
    user_request: str,
    available_templates: List[str],
    resource_constraints: Optional[dict] = None,
    provider: Optional[str] = Query(None, description="Specific LLM provider to use"),
    service: LLMService = Depends(get_llm_service)
) -> LLMResponse:
    """Analyze requirements using LLM."""
    try:
        result = await service.analyze_requirements(
            user_request=user_request,
            available_templates=available_templates,
            resource_constraints=resource_constraints or {}
        )
        
        return LLMResponse(
            success=result["success"],
            result=result.get("specification"),
            request_id=f"req-{hash(user_request)}", # Simple ID for demo
            provider_used=result.get("provider_used", "unknown"),
            model_used="unknown",  # Will be filled by actual service
            response_time_ms=0.0,  # Will be measured by actual service
            error_message=result.get("error") if not result["success"] else None
        )
    except Exception as e:
        logger.error(f"LLM requirements analysis failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post(
    "/generate-iac", 
    response_model=LLMResponse,
    summary="Generate Infrastructure as Code",
    description="Use LLM to generate IaC configurations from deployment specification."
)
async def generate_iac_llm(
    deployment_spec: dict,
    template_base: str,
    target_platform: str = "proxmox",
    existing_resources: Optional[dict] = None,
    provider: Optional[str] = Query(None, description="Specific LLM provider to use"),
    service: LLMService = Depends(get_llm_service)
) -> LLMResponse:
    """Generate IaC using LLM."""
    try:
        result = await service.generate_iac(
            deployment_spec=deployment_spec,
            template_base=template_base,
            target_platform=target_platform,
            existing_resources=existing_resources
        )
        
        return LLMResponse(
            success=result["success"],
            result=result.get("files"),
            request_id=f"iac-{hash(str(deployment_spec))}", # Simple ID for demo
            provider_used=result.get("provider_used", "unknown"),
            model_used="unknown",
            response_time_ms=0.0,
            error_message=result.get("error") if not result["success"] else None
        )
    except Exception as e:
        logger.error(f"LLM IaC generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post(
    "/diagnose-error",
    response_model=ErrorDiagnosisResponse,
    summary="Diagnose deployment errors",
    description="Use LLM to diagnose and provide solutions for deployment errors."
)
async def diagnose_error_llm(
    request: ErrorDiagnosisRequest,
    provider: Optional[str] = Query(None, description="Specific LLM provider to use"),
    service: LLMService = Depends(get_llm_service)
) -> ErrorDiagnosisResponse:
    """Diagnose errors using LLM."""
    try:
        result = await service.diagnose_error(
            error_logs=request.error_logs,
            deployment_config=request.deployment_config,
            system_state=request.system_state,
            previous_fixes=request.previous_fixes
        )
        
        if result["success"]:
            diagnosis = result["diagnosis"]
            return ErrorDiagnosisResponse(
                success=True,
                diagnosis_id=f"diag-{hash(request.error_logs)}",
                error_analysis=diagnosis.get("error_analysis"),
                immediate_actions=diagnosis.get("immediate_actions", []),
                root_cause_fixes=diagnosis.get("root_cause_fixes", []),
                monitoring_recommendations=diagnosis.get("monitoring_recommendations", []),
                confidence_score=diagnosis.get("confidence_score", 0.0),
                estimated_resolution_time=diagnosis.get("estimated_resolution_time"),
                requires_manual_intervention=diagnosis.get("requires_manual_intervention", False),
                provider_used=result.get("provider_used", "unknown")
            )
        else:
            return ErrorDiagnosisResponse(
                success=False,
                diagnosis_id=f"diag-{hash(request.error_logs)}",
                provider_used=result.get("provider_used", "unknown"),
                error_message=result.get("error", "Unknown error")
            )
            
    except Exception as e:
        logger.error(f"LLM error diagnosis failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/providers/status",
    response_model=List[LLMProviderStatus],
    summary="Get LLM provider status",
    description="Get the status of all configured LLM providers."
)
async def get_provider_status(
    service: LLMService = Depends(get_llm_service)
) -> List[LLMProviderStatus]:
    """Get LLM provider status."""
    try:
        status_info = service.get_provider_status()
        
        # Convert to LLMProviderStatus objects
        providers = []
        for name, info in status_info.items():
            providers.append(LLMProviderStatus(
                provider_name=name,
                available=info["available"],
                primary=info.get("primary", False),
                fallback=info.get("fallback", False),
                error_message=info.get("error") if not info["available"] else None
            ))
        
        return providers
    except Exception as e:
        logger.error(f"Failed to get provider status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/health",
    response_model=LLMHealthCheck,
    summary="LLM service health check",
    description="Get overall health status of the LLM service."
)
async def health_check(
    service: LLMService = Depends(get_llm_service)
) -> LLMHealthCheck:
    """LLM service health check."""
    try:
        status_info = service.get_provider_status()
        
        # Determine overall health
        available_providers = [name for name, info in status_info.items() if info["available"]]
        primary_healthy = any(info.get("primary") and info["available"] for info in status_info.values())
        
        overall_status = "healthy" if primary_healthy else "degraded" if available_providers else "unhealthy"
        
        return LLMHealthCheck(
            overall_status=overall_status,
            providers=status_info,
            primary_provider_healthy=primary_healthy,
            fallback_available=len(available_providers) > 1,
            average_response_time=0.0,  # Would be calculated from metrics
            success_rate=1.0,  # Would be calculated from metrics
            error_rate=0.0,  # Would be calculated from metrics
            requests_per_minute=0.0,  # Would be calculated from metrics
            tokens_per_minute=0.0,  # Would be calculated from metrics
            issues=[],  # Would be populated based on actual issues
            recommendations=[]  # Would be populated based on analysis
        )
    except Exception as e:
        logger.error(f"LLM health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post(
    "/request",
    response_model=LLMResponse,
    summary="Generic LLM request",
    description="Make a generic request to the LLM service."
)
async def llm_request(
    request: LLMRequest,
    service: LLMService = Depends(get_llm_service)
) -> LLMResponse:
    """Generic LLM request."""
    try:
        # Route to appropriate method based on operation
        if request.operation == "analyze_requirements":
            result = await service.analyze_requirements(**request.parameters)
        elif request.operation == "generate_iac":
            result = await service.generate_iac(**request.parameters)
        elif request.operation == "diagnose_error":
            result = await service.diagnose_error(**request.parameters)
        else:
            raise ValueError(f"Unknown operation: {request.operation}")
        
        return LLMResponse(
            success=result.get("success", False),
            result=result,
            request_id=f"{request.operation}-{hash(str(request.parameters))}",
            provider_used=result.get("provider_used", "unknown"),
            model_used="unknown",
            response_time_ms=0.0
        )
    except Exception as e:
        logger.error(f"LLM request failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/usage",
    response_model=List[LLMUsageStats],
    summary="Get LLM usage statistics",
    description="Get usage statistics for LLM providers."
)
async def get_usage_stats(
    provider: Optional[str] = Query(None, description="Filter by provider"),
    time_period: str = Query("24h", description="Time period (1h, 24h, 7d, 30d)"),
    service: LLMService = Depends(get_llm_service)
) -> List[LLMUsageStats]:
    """Get LLM usage statistics."""
    try:
        # This would be implemented to return actual usage stats
        # For now, return empty list
        return []
    except Exception as e:
        logger.error(f"Failed to get usage stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/templates",
    response_model=List[LLMPromptTemplate],
    summary="Get prompt templates",
    description="Get available LLM prompt templates."
)
async def get_prompt_templates(
    category: Optional[str] = Query(None, description="Filter by category"),
    service: LLMService = Depends(get_llm_service)
) -> List[LLMPromptTemplate]:
    """Get prompt templates."""
    try:
        # This would return actual prompt templates
        # For now, return empty list
        return []
    except Exception as e:
        logger.error(f"Failed to get prompt templates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )