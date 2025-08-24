"""Deployment management API endpoints."""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse

from backend.core.exceptions import AIDException
from backend.core.services.deployment_service import DeploymentService
from backend.models.schemas import (
    DeploymentListResponse,
    DeploymentLogs,
    DeploymentMetrics,
    DeploymentRequest,
    DeploymentResponse,
    DeploymentUpdateRequest,
)

logger = logging.getLogger(__name__)
router = APIRouter()


def get_deployment_service() -> DeploymentService:
    """Dependency to get deployment service instance."""
    # This will be implemented when we create the service layer
    # For now, return a placeholder
    raise NotImplementedError("DeploymentService not yet implemented")


@router.post(
    "/",
    response_model=DeploymentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new deployment",
    description="Create a new infrastructure deployment from natural language requirements.",
)
async def create_deployment(
    request: DeploymentRequest,
    service: DeploymentService = Depends(get_deployment_service),
) -> DeploymentResponse:
    """Create a new deployment."""
    try:
        deployment = await service.create_deployment(request)
        return deployment
    except AIDException as e:
        logger.error(f"Deployment creation failed: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error creating deployment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get(
    "/",
    response_model=DeploymentListResponse,
    summary="List deployments",
    description="Get a paginated list of all deployments.",
)
async def list_deployments(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status_filter: Optional[str] = Query(
        None, description="Filter by deployment status"
    ),
    service_type: Optional[str] = Query(None, description="Filter by service type"),
    service: DeploymentService = Depends(get_deployment_service),
) -> DeploymentListResponse:
    """List deployments with optional filtering."""
    try:
        deployments = await service.list_deployments(
            page=page,
            page_size=page_size,
            status_filter=status_filter,
            service_type=service_type,
        )
        return deployments
    except AIDException as e:
        logger.error(f"Failed to list deployments: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error listing deployments: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get(
    "/{deployment_id}",
    response_model=DeploymentResponse,
    summary="Get deployment details",
    description="Get detailed information about a specific deployment.",
)
async def get_deployment(
    deployment_id: str, service: DeploymentService = Depends(get_deployment_service)
) -> DeploymentResponse:
    """Get deployment by ID."""
    try:
        deployment = await service.get_deployment(deployment_id)
        if not deployment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Deployment {deployment_id} not found",
            )
        return deployment
    except HTTPException:
        raise
    except AIDException as e:
        logger.error(f"Failed to get deployment {deployment_id}: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error getting deployment {deployment_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.put(
    "/{deployment_id}",
    response_model=DeploymentResponse,
    summary="Update deployment",
    description="Update an existing deployment configuration.",
)
async def update_deployment(
    deployment_id: str,
    request: DeploymentUpdateRequest,
    service: DeploymentService = Depends(get_deployment_service),
) -> DeploymentResponse:
    """Update deployment."""
    try:
        deployment = await service.update_deployment(deployment_id, request)
        return deployment
    except AIDException as e:
        logger.error(f"Failed to update deployment {deployment_id}: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error updating deployment {deployment_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.delete(
    "/{deployment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete deployment",
    description="Delete a deployment and clean up all associated resources.",
)
async def delete_deployment(
    deployment_id: str,
    force: bool = Query(False, description="Force delete even if resources are in use"),
    service: DeploymentService = Depends(get_deployment_service),
) -> None:
    """Delete deployment."""
    try:
        await service.delete_deployment(deployment_id, force=force)
    except AIDException as e:
        logger.error(f"Failed to delete deployment {deployment_id}: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error deleting deployment {deployment_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post(
    "/{deployment_id}/start",
    response_model=DeploymentResponse,
    summary="Start deployment",
    description="Start a stopped deployment.",
)
async def start_deployment(
    deployment_id: str, service: DeploymentService = Depends(get_deployment_service)
) -> DeploymentResponse:
    """Start deployment."""
    try:
        deployment = await service.start_deployment(deployment_id)
        return deployment
    except AIDException as e:
        logger.error(f"Failed to start deployment {deployment_id}: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error starting deployment {deployment_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post(
    "/{deployment_id}/stop",
    response_model=DeploymentResponse,
    summary="Stop deployment",
    description="Stop a running deployment.",
)
async def stop_deployment(
    deployment_id: str,
    graceful: bool = Query(True, description="Graceful shutdown"),
    service: DeploymentService = Depends(get_deployment_service),
) -> DeploymentResponse:
    """Stop deployment."""
    try:
        deployment = await service.stop_deployment(deployment_id, graceful=graceful)
        return deployment
    except AIDException as e:
        logger.error(f"Failed to stop deployment {deployment_id}: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error stopping deployment {deployment_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post(
    "/{deployment_id}/restart",
    response_model=DeploymentResponse,
    summary="Restart deployment",
    description="Restart a deployment.",
)
async def restart_deployment(
    deployment_id: str, service: DeploymentService = Depends(get_deployment_service)
) -> DeploymentResponse:
    """Restart deployment."""
    try:
        deployment = await service.restart_deployment(deployment_id)
        return deployment
    except AIDException as e:
        logger.error(f"Failed to restart deployment {deployment_id}: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error restarting deployment {deployment_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get(
    "/{deployment_id}/metrics",
    response_model=DeploymentMetrics,
    summary="Get deployment metrics",
    description="Get real-time metrics for a deployment.",
)
async def get_deployment_metrics(
    deployment_id: str, service: DeploymentService = Depends(get_deployment_service)
) -> DeploymentMetrics:
    """Get deployment metrics."""
    try:
        metrics = await service.get_deployment_metrics(deployment_id)
        return metrics
    except AIDException as e:
        logger.error(f"Failed to get metrics for deployment {deployment_id}: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(
            f"Unexpected error getting metrics for deployment {deployment_id}: {e}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get(
    "/{deployment_id}/logs",
    response_model=DeploymentLogs,
    summary="Get deployment logs",
    description="Get logs for a deployment.",
)
async def get_deployment_logs(
    deployment_id: str,
    lines: int = Query(
        100, ge=1, le=10000, description="Number of log lines to return"
    ),
    follow: bool = Query(False, description="Follow log output"),
    service: DeploymentService = Depends(get_deployment_service),
) -> DeploymentLogs:
    """Get deployment logs."""
    try:
        logs = await service.get_deployment_logs(
            deployment_id, lines=lines, follow=follow
        )
        return logs
    except AIDException as e:
        logger.error(f"Failed to get logs for deployment {deployment_id}: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(
            f"Unexpected error getting logs for deployment {deployment_id}: {e}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get(
    "/{deployment_id}/status",
    summary="Get deployment status",
    description="Get the current status of a deployment.",
)
async def get_deployment_status(
    deployment_id: str, service: DeploymentService = Depends(get_deployment_service)
) -> JSONResponse:
    """Get deployment status."""
    try:
        status_info = await service.get_deployment_status(deployment_id)
        return JSONResponse(content=status_info)
    except AIDException as e:
        logger.error(f"Failed to get status for deployment {deployment_id}: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(
            f"Unexpected error getting status for deployment {deployment_id}: {e}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
