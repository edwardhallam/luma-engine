"""Requirements analysis API endpoints."""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse

from backend.core.exceptions import AIDException
from backend.core.services.requirement_service import RequirementService
from backend.models.schemas import (
    RequirementAnalysisRequest,
    RequirementAnalysisResponse,
    RequirementHistory,
    RequirementInsight,
    RequirementRefinementRequest,
    RequirementTemplate,
    RequirementValidation,
)

logger = logging.getLogger(__name__)
router = APIRouter()


def get_requirement_service() -> RequirementService:
    """Dependency to get requirement service instance."""
    # This will be implemented when we create the service layer
    raise NotImplementedError("RequirementService not yet implemented")


@router.post(
    "/analyze",
    response_model=RequirementAnalysisResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Analyze requirements",
    description="Analyze natural language requirements and generate deployment specification.",
)
async def analyze_requirements(
    request: RequirementAnalysisRequest,
    service: RequirementService = Depends(get_requirement_service),
) -> RequirementAnalysisResponse:
    """Analyze user requirements."""
    try:
        analysis = await service.analyze_requirements(request)
        return analysis
    except AIDException as e:
        logger.error(f"Requirements analysis failed: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error in requirements analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post(
    "/refine",
    response_model=RequirementAnalysisResponse,
    summary="Refine requirements",
    description="Refine an existing requirements analysis based on user feedback.",
)
async def refine_requirements(
    request: RequirementRefinementRequest,
    service: RequirementService = Depends(get_requirement_service),
) -> RequirementAnalysisResponse:
    """Refine requirements analysis."""
    try:
        refined_analysis = await service.refine_requirements(request)
        return refined_analysis
    except AIDException as e:
        logger.error(f"Requirements refinement failed: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error in requirements refinement: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post(
    "/validate",
    response_model=RequirementValidation,
    summary="Validate requirements",
    description="Validate a deployment specification for correctness and completeness.",
)
async def validate_requirements(
    specification: dict,
    target_platform: str = Query("proxmox", description="Target deployment platform"),
    service: RequirementService = Depends(get_requirement_service),
) -> RequirementValidation:
    """Validate requirements specification."""
    try:
        validation = await service.validate_requirements(specification, target_platform)
        return validation
    except AIDException as e:
        logger.error(f"Requirements validation failed: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error in requirements validation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get(
    "/templates",
    response_model=List[RequirementTemplate],
    summary="Get requirement templates",
    description="Get available requirement templates for common patterns.",
)
async def get_requirement_templates(
    category: Optional[str] = Query(None, description="Filter by category"),
    service: RequirementService = Depends(get_requirement_service),
) -> List[RequirementTemplate]:
    """Get requirement templates."""
    try:
        templates = await service.get_requirement_templates(category)
        return templates
    except AIDException as e:
        logger.error(f"Failed to get requirement templates: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error getting requirement templates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get(
    "/templates/{template_id}",
    response_model=RequirementTemplate,
    summary="Get requirement template",
    description="Get a specific requirement template by ID.",
)
async def get_requirement_template(
    template_id: str, service: RequirementService = Depends(get_requirement_service)
) -> RequirementTemplate:
    """Get requirement template by ID."""
    try:
        template = await service.get_requirement_template(template_id)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Requirement template {template_id} not found",
            )
        return template
    except HTTPException:
        raise
    except AIDException as e:
        logger.error(f"Failed to get requirement template {template_id}: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(
            f"Unexpected error getting requirement template {template_id}: {e}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post(
    "/templates",
    response_model=RequirementTemplate,
    status_code=status.HTTP_201_CREATED,
    summary="Create requirement template",
    description="Create a new requirement template from a successful analysis.",
)
async def create_requirement_template(
    template_data: dict, service: RequirementService = Depends(get_requirement_service)
) -> RequirementTemplate:
    """Create requirement template."""
    try:
        template = await service.create_requirement_template(template_data)
        return template
    except AIDException as e:
        logger.error(f"Failed to create requirement template: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error creating requirement template: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get(
    "/history",
    response_model=List[RequirementHistory],
    summary="Get requirements history",
    description="Get history of requirements analyses.",
)
async def get_requirements_history(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    service: RequirementService = Depends(get_requirement_service),
) -> List[RequirementHistory]:
    """Get requirements history."""
    try:
        history = await service.get_requirements_history(
            page=page, page_size=page_size, user_id=user_id
        )
        return history
    except AIDException as e:
        logger.error(f"Failed to get requirements history: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error getting requirements history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get(
    "/history/{analysis_id}",
    response_model=RequirementHistory,
    summary="Get requirements analysis history",
    description="Get detailed history of a specific requirements analysis.",
)
async def get_requirement_history(
    analysis_id: str, service: RequirementService = Depends(get_requirement_service)
) -> RequirementHistory:
    """Get requirement analysis history."""
    try:
        history = await service.get_requirement_history(analysis_id)
        if not history:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Requirements analysis {analysis_id} not found",
            )
        return history
    except HTTPException:
        raise
    except AIDException as e:
        logger.error(f"Failed to get requirement history {analysis_id}: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error getting requirement history {analysis_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get(
    "/insights",
    response_model=List[RequirementInsight],
    summary="Get requirement insights",
    description="Get insights derived from requirements analysis patterns.",
)
async def get_requirement_insights(
    insight_type: Optional[str] = Query(None, description="Filter by insight type"),
    min_frequency: int = Query(1, ge=1, description="Minimum frequency threshold"),
    service: RequirementService = Depends(get_requirement_service),
) -> List[RequirementInsight]:
    """Get requirement insights."""
    try:
        insights = await service.get_requirement_insights(
            insight_type=insight_type, min_frequency=min_frequency
        )
        return insights
    except AIDException as e:
        logger.error(f"Failed to get requirement insights: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error getting requirement insights: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post(
    "/{analysis_id}/feedback",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Provide feedback",
    description="Provide feedback on a requirements analysis for learning purposes.",
)
async def provide_feedback(
    analysis_id: str,
    feedback: dict,
    service: RequirementService = Depends(get_requirement_service),
) -> None:
    """Provide feedback on requirements analysis."""
    try:
        await service.provide_feedback(analysis_id, feedback)
    except AIDException as e:
        logger.error(f"Failed to save feedback for analysis {analysis_id}: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(
            f"Unexpected error saving feedback for analysis {analysis_id}: {e}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get(
    "/suggestions",
    summary="Get requirement suggestions",
    description="Get AI-powered suggestions for improving requirements.",
)
async def get_requirement_suggestions(
    partial_request: str = Query(..., description="Partial requirement text"),
    context: Optional[str] = Query(None, description="Additional context"),
    service: RequirementService = Depends(get_requirement_service),
) -> JSONResponse:
    """Get requirement suggestions."""
    try:
        suggestions = await service.get_requirement_suggestions(
            partial_request, context
        )
        return JSONResponse(content=suggestions)
    except AIDException as e:
        logger.error(f"Failed to get requirement suggestions: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error getting requirement suggestions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
