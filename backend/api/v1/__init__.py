"""API v1 module."""

from fastapi import APIRouter
from .deployments import router as deployments_router
from .templates import router as templates_router
from .requirements import router as requirements_router
from .llm import router as llm_router

api_router = APIRouter(prefix="/api/v1")

# Include all routers
api_router.include_router(deployments_router, prefix="/deployments", tags=["deployments"])
api_router.include_router(templates_router, prefix="/templates", tags=["templates"])
api_router.include_router(requirements_router, prefix="/requirements", tags=["requirements"])
api_router.include_router(llm_router, prefix="/llm", tags=["llm"])

__all__ = ["api_router"]