"""Main FastAPI application for LumaEngine."""

import logging
import sys
import time
from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.api.v1 import api_router
from backend.core.config import settings
from backend.core.exceptions import AIDException

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        *([logging.FileHandler(settings.log_file)] if settings.log_file else []),
    ],
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")

    # Initialize services here
    await startup_services()

    yield

    # Shutdown
    logger.info("Shutting down application")
    await shutdown_services()


async def startup_services():
    """Initialize application services."""
    try:
        # Initialize database
        await init_database()

        # Initialize LLM services
        await init_llm_services()

        # Initialize infrastructure clients
        await init_infrastructure_clients()

        # Initialize monitoring
        if settings.enable_metrics:
            await init_monitoring()

        logger.info("All services initialized successfully")

    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise


async def shutdown_services():
    """Cleanup application services."""
    try:
        # Cleanup database connections
        await cleanup_database()

        # Cleanup external clients
        await cleanup_clients()

        logger.info("All services cleaned up successfully")

    except Exception as e:
        logger.error(f"Error during cleanup: {e}")


async def init_database():
    """Initialize database connection."""
    # This will be implemented when we create the database layer
    logger.info("Database initialization placeholder")


async def init_llm_services():
    """Initialize LLM services."""
    try:
        from backend.llm.service import LLMService

        LLMService(settings.llm_config)  # Initialize and test
        logger.info("LLM services initialized")
    except ImportError as e:
        logger.warning(f"LLM services not available (missing dependencies): {e}")
    except Exception as e:
        logger.warning(f"LLM services initialization failed: {e}")


async def init_infrastructure_clients():
    """Initialize infrastructure clients."""
    # Initialize Proxmox client
    if settings.proxmox_config:
        logger.info("Proxmox client would be initialized here")

    # Initialize GitLab client
    if settings.gitlab_config:
        logger.info("GitLab client would be initialized here")

    # Initialize MinIO client
    logger.info("MinIO client would be initialized here")


async def init_monitoring():
    """Initialize monitoring and metrics."""
    logger.info("Monitoring initialization placeholder")


async def cleanup_database():
    """Cleanup database connections."""
    logger.info("Database cleanup placeholder")


async def cleanup_clients():
    """Cleanup external clients."""
    logger.info("Clients cleanup placeholder")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Next-generation AI-powered infrastructure orchestration platform",
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

# Add trusted host middleware in production
if settings.is_production:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"],  # Configure with actual hosts in production
    )


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add process time header to responses."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Exception handlers
@app.exception_handler(AIDException)
async def aid_exception_handler(request: Request, exc: AIDException):
    """Handle custom AID exceptions."""
    logger.error(f"AID Exception: {exc.message}", extra={"details": exc.details})
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "details": exc.details,
            "type": exc.__class__.__name__,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors."""
    logger.warning(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "details": exc.errors(),
            "type": "RequestValidationError",
        },
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions."""
    logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "type": "HTTPException"},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "type": "InternalServerError"},
    )


# Health check endpoint
@app.get("/health", tags=["system"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "environment": settings.environment,
        "timestamp": time.time(),
    }


# Info endpoint
@app.get("/info", tags=["system"])
async def app_info():
    """Application information endpoint."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "debug": settings.debug,
        "features": {
            "metrics": settings.enable_metrics,
            "tracing": settings.enable_tracing,
            "caching": settings.enable_caching,
            "rate_limiting": settings.enable_rate_limiting,
        },
    }


# Metrics endpoint
@app.get("/metrics", tags=["system"])
async def metrics():
    """Prometheus metrics endpoint."""
    if not settings.enable_metrics:
        raise HTTPException(status_code=404, detail="Metrics not enabled")

    # This would return Prometheus metrics
    return {"message": "Metrics endpoint - implementation pending"}


# Include API routers
app.include_router(api_router, prefix=settings.api_prefix)


# Root endpoint
@app.get("/", tags=["system"])
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs_url": "/docs" if settings.debug else None,
        "api_prefix": settings.api_prefix,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload and settings.is_development,
        log_level=settings.log_level.lower(),
        access_log=True,
    )
