"""System API endpoints."""

import time
from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from backend.core.config import settings

router = APIRouter()


@router.get("/health")
async def system_health() -> Dict[str, Any]:
    """System health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "environment": settings.environment,
        "timestamp": time.time(),
    }


@router.get("/info")
async def system_info() -> Dict[str, Any]:
    """System information endpoint."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "debug": settings.debug,
        "features": {
            "metrics": settings.enable_metrics,
            "tracing": settings.enable_tracing,
            "caching": settings.enable_caching,
            "rate_limiting": getattr(settings, "enable_rate_limiting", False),
        },
    }


@router.get("/status")
async def system_status() -> Dict[str, Any]:
    """Detailed system status."""
    # TODO: Add actual service status checks
    return {
        "status": "operational",
        "services": {
            "api": "healthy",
            "database": "unknown",  # Will be implemented when DB is added
            "llm": "healthy",
            "cache": "unknown",
        },
        "uptime": time.time(),  # This should be actual uptime
        "version": settings.app_version,
    }
