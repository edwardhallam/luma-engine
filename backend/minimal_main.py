"""Minimal FastAPI app for quick start - no external dependencies."""

import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.minimal_config import settings

# Create minimal FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="LumaEngine - Quick Start Mode",
    version=settings.app_version,
    debug=settings.debug,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.app_name} (Quick Start Mode)",
        "version": settings.app_version,
        "docs_url": "/docs",
        "mode": "minimal",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "environment": settings.environment,
        "mode": "minimal",
        "timestamp": time.time(),
    }


@app.get("/api/v1/status")
async def api_status():
    """API status endpoint."""
    return {
        "api": "available",
        "version": "v1",
        "mode": "minimal",
        "features": {
            "llm": "disabled (quick start mode)",
            "infrastructure": "disabled (quick start mode)",
            "database": "disabled (quick start mode)",
        },
    }


@app.get("/api/v1/hello")
async def hello_world():
    """Simple test endpoint."""
    return {
        "message": "Hello from LumaEngine!",
        "timestamp": time.time(),
        "mode": "minimal",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.minimal_main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
    )
