"""Template management API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, status, File, UploadFile
from fastapi.responses import JSONResponse

from backend.models.schemas import (
    Template,
    TemplateRequest,
    TemplateResponse,
    TemplateListResponse,
    TemplateValidationRequest,
    TemplateValidationResponse,
    TemplateUsageStats,
    TemplateCategory,
    TemplateStatus,
)
from backend.core.exceptions import AIDException
from backend.core.services.template_service import TemplateService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


def get_template_service() -> TemplateService:
    """Dependency to get template service instance."""
    # This will be implemented when we create the service layer
    raise NotImplementedError("TemplateService not yet implemented")


@router.get(
    "/",
    response_model=TemplateListResponse,
    summary="List templates",
    description="Get a paginated list of all available templates."
)
async def list_templates(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    category: Optional[TemplateCategory] = Query(None, description="Filter by category"),
    status: Optional[TemplateStatus] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search in template name and description"),
    tags: Optional[str] = Query(None, description="Filter by tags (comma-separated)"),
    service: TemplateService = Depends(get_template_service)
) -> TemplateListResponse:
    """List templates with optional filtering."""
    try:
        templates = await service.list_templates(
            page=page,
            page_size=page_size,
            category=category,
            status=status,
            search=search,
            tags=tags.split(",") if tags else None
        )
        return templates
    except AIDException as e:
        logger.error(f"Failed to list templates: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error listing templates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get(
    "/{template_id}",
    response_model=TemplateResponse,
    summary="Get template details",
    description="Get detailed information about a specific template."
)
async def get_template(
    template_id: str,
    include_preview: bool = Query(False, description="Include deployment preview"),
    service: TemplateService = Depends(get_template_service)
) -> TemplateResponse:
    """Get template by ID."""
    try:
        template = await service.get_template(template_id, include_preview=include_preview)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Template {template_id} not found"
            )
        return template
    except HTTPException:
        raise
    except AIDException as e:
        logger.error(f"Failed to get template {template_id}: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error getting template {template_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post(
    "/",
    response_model=TemplateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create template",
    description="Create a new infrastructure template."
)
async def create_template(
    request: TemplateRequest,
    service: TemplateService = Depends(get_template_service)
) -> TemplateResponse:
    """Create a new template."""
    try:
        template = await service.create_template(request)
        return template
    except AIDException as e:
        logger.error(f"Template creation failed: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error creating template: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put(
    "/{template_id}",
    response_model=TemplateResponse,
    summary="Update template",
    description="Update an existing template."
)
async def update_template(
    template_id: str,
    request: TemplateRequest,
    service: TemplateService = Depends(get_template_service)
) -> TemplateResponse:
    """Update template."""
    try:
        template = await service.update_template(template_id, request)
        return template
    except AIDException as e:
        logger.error(f"Failed to update template {template_id}: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error updating template {template_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete(
    "/{template_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete template",
    description="Delete a template (only if not in use)."
)
async def delete_template(
    template_id: str,
    force: bool = Query(False, description="Force delete even if in use"),
    service: TemplateService = Depends(get_template_service)
) -> None:
    """Delete template."""
    try:
        await service.delete_template(template_id, force=force)
    except AIDException as e:
        logger.error(f"Failed to delete template {template_id}: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error deleting template {template_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post(
    "/validate",
    response_model=TemplateValidationResponse,
    summary="Validate template",
    description="Validate a template for syntax and configuration correctness."
)
async def validate_template(
    request: TemplateValidationRequest,
    service: TemplateService = Depends(get_template_service)
) -> TemplateValidationResponse:
    """Validate template."""
    try:
        validation = await service.validate_template(request)
        return validation
    except AIDException as e:
        logger.error(f"Template validation failed: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error validating template: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post(
    "/import",
    response_model=TemplateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Import template",
    description="Import a template from a file or URL."
)
async def import_template(
    file: UploadFile = File(..., description="Template file to import"),
    service: TemplateService = Depends(get_template_service)
) -> TemplateResponse:
    """Import template from file."""
    try:
        content = await file.read()
        template = await service.import_template(content, file.filename)
        return template
    except AIDException as e:
        logger.error(f"Template import failed: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error importing template: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get(
    "/{template_id}/export",
    summary="Export template",
    description="Export a template as a downloadable file."
)
async def export_template(
    template_id: str,
    format: str = Query("json", description="Export format (json, yaml, tar)"),
    service: TemplateService = Depends(get_template_service)
):
    """Export template."""
    try:
        export_data = await service.export_template(template_id, format)
        return export_data
    except AIDException as e:
        logger.error(f"Failed to export template {template_id}: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error exporting template {template_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get(
    "/{template_id}/usage",
    response_model=TemplateUsageStats,
    summary="Get template usage statistics",
    description="Get usage statistics for a template."
)
async def get_template_usage(
    template_id: str,
    service: TemplateService = Depends(get_template_service)
) -> TemplateUsageStats:
    """Get template usage statistics."""
    try:
        stats = await service.get_template_usage(template_id)
        return stats
    except AIDException as e:
        logger.error(f"Failed to get usage stats for template {template_id}: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error getting usage stats for template {template_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post(
    "/{template_id}/clone",
    response_model=TemplateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Clone template",
    description="Create a copy of an existing template."
)
async def clone_template(
    template_id: str,
    new_name: str = Query(..., description="Name for the cloned template"),
    service: TemplateService = Depends(get_template_service)
) -> TemplateResponse:
    """Clone template."""
    try:
        template = await service.clone_template(template_id, new_name)
        return template
    except AIDException as e:
        logger.error(f"Failed to clone template {template_id}: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error cloning template {template_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get(
    "/categories",
    response_model=List[str],
    summary="Get template categories",
    description="Get all available template categories."
)
async def get_template_categories(
    service: TemplateService = Depends(get_template_service)
) -> List[str]:
    """Get template categories."""
    try:
        categories = await service.get_template_categories()
        return categories
    except AIDException as e:
        logger.error(f"Failed to get template categories: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error getting template categories: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get(
    "/search",
    response_model=TemplateListResponse,
    summary="Search templates",
    description="Search templates using various criteria."
)
async def search_templates(
    query: str = Query(..., description="Search query"),
    category: Optional[TemplateCategory] = Query(None, description="Category filter"),
    min_rating: Optional[float] = Query(None, ge=0.0, le=5.0, description="Minimum rating"),
    service: TemplateService = Depends(get_template_service)
) -> TemplateListResponse:
    """Search templates."""
    try:
        results = await service.search_templates(
            query=query,
            category=category,
            min_rating=min_rating
        )
        return results
    except AIDException as e:
        logger.error(f"Template search failed: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error searching templates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get(
    "/recommended",
    response_model=List[Template],
    summary="Get recommended templates",
    description="Get templates recommended based on usage patterns and user preferences."
)
async def get_recommended_templates(
    limit: int = Query(10, ge=1, le=50, description="Number of recommendations"),
    user_context: Optional[str] = Query(None, description="User context for personalization"),
    service: TemplateService = Depends(get_template_service)
) -> List[Template]:
    """Get recommended templates."""
    try:
        recommendations = await service.get_recommended_templates(
            limit=limit,
            user_context=user_context
        )
        return recommendations
    except AIDException as e:
        logger.error(f"Failed to get template recommendations: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error getting template recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )