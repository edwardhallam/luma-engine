"""API v1 module."""

from fastapi import APIRouter

try:
    from .deployments import router as deployments_router
except ImportError:
    deployments_router = None

try:
    from .iac import router as iac_router
except ImportError:
    iac_router = None

try:
    from .llm import router as llm_router
except ImportError:
    llm_router = None

try:
    from .requirements import router as requirements_router
except ImportError:
    requirements_router = None

try:
    from .security import router as security_router
except ImportError:
    security_router = None

try:
    from .templates import router as templates_router
except ImportError:
    templates_router = None

try:
    from .system import router as system_router
except ImportError:
    system_router = None

api_router = APIRouter()


# Basic test endpoint
@api_router.get("/test")
async def test_endpoint():
    return {"message": "API is working", "status": "ok"}


# Include available routers
if deployments_router:
    api_router.include_router(
        deployments_router, prefix="/deployments", tags=["deployments"]
    )

if iac_router:
    api_router.include_router(iac_router, prefix="/iac", tags=["iac"])

if templates_router:
    api_router.include_router(templates_router, prefix="/templates", tags=["templates"])

if requirements_router:
    api_router.include_router(
        requirements_router, prefix="/requirements", tags=["requirements"]
    )

if llm_router:
    api_router.include_router(llm_router, prefix="/llm", tags=["llm"])

if security_router:
    api_router.include_router(security_router, prefix="/security", tags=["security"])

if system_router:
    api_router.include_router(system_router, prefix="/system", tags=["system"])

__all__ = ["api_router"]
