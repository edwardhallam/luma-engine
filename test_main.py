"""Simplified main app for testing without LLM dependencies."""

import time
import logging
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple configuration
class TestSettings:
    app_name = "AI Infrastructure Deployer (Test)"
    app_version = "0.1.0"
    debug = True
    environment = "test"
    
settings = TestSettings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI-powered infrastructure deployment platform (Test Mode)",
    version=settings.app_version,
    debug=settings.debug,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple models for testing
class RequirementAnalysisRequest(BaseModel):
    user_request: str
    context: Dict[str, Any] = {}

class RequirementAnalysisResponse(BaseModel):
    success: bool
    analysis_id: str
    specification: Dict[str, Any] = {}
    confidence_score: float = 0.8
    provider_used: str = "test"

# Test endpoints
@app.get("/", tags=["system"])
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "status": "running",
        "docs_url": "/docs"
    }

@app.get("/health", tags=["system"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "environment": settings.environment,
        "timestamp": time.time()
    }

@app.get("/api/v1/llm/providers/status", tags=["llm"])
async def get_provider_status():
    """Mock LLM provider status."""
    return [
        {
            "provider_name": "test",
            "available": True,
            "primary": True,
            "fallback": False,
            "model": "test-model",
            "last_check": time.time(),
            "response_time_ms": 100.0
        }
    ]

@app.post("/api/v1/requirements/analyze", tags=["requirements"])
async def analyze_requirements(request: RequirementAnalysisRequest) -> RequirementAnalysisResponse:
    """Mock requirements analysis."""
    logger.info(f"Analyzing request: {request.user_request}")
    
    # Simple mock analysis based on keywords
    spec = {
        "service_type": "web-application",
        "service_name": "test-service",
        "description": f"Generated from: {request.user_request}",
        "template": "basic",
        "resource_requirements": {
            "cpu_cores": 2.0,
            "memory_gb": 4.0,
            "storage_gb": 50.0,
            "gpu_required": False
        }
    }
    
    # Adjust based on keywords
    if "chat" in request.user_request.lower():
        spec["service_type"] = "chat-service"
        spec["template"] = "librechat"
        
    if "database" in request.user_request.lower():
        spec["dependencies"] = [
            {"service": "postgresql", "type": "database", "required": True}
        ]
    
    return RequirementAnalysisResponse(
        success=True,
        analysis_id=f"test-{int(time.time())}",
        specification=spec,
        confidence_score=0.85
    )

@app.get("/api/v1/templates", tags=["templates"])
async def list_templates():
    """Mock template listing."""
    return {
        "templates": [
            {
                "template_id": "librechat",
                "name": "LibreChat",
                "description": "Chat interface with LLM support",
                "category": "chat-services",
                "status": "active"
            },
            {
                "template_id": "postgresql",
                "name": "PostgreSQL Database",
                "description": "PostgreSQL database server",
                "category": "databases", 
                "status": "active"
            }
        ],
        "total": 2,
        "page": 1,
        "page_size": 20
    }

@app.post("/api/v1/deployments", tags=["deployments"])
async def create_deployment(deployment_data: Dict[str, Any]):
    """Mock deployment creation."""
    return {
        "deployment_id": f"deploy-{int(time.time())}",
        "status": "pending",
        "specification": deployment_data,
        "created_at": time.time(),
        "progress": 0
    }

@app.get("/api/v1/deployments", tags=["deployments"])
async def list_deployments():
    """Mock deployment listing."""
    return {
        "deployments": [
            {
                "deployment_id": "deploy-12345",
                "status": "running",
                "service_name": "test-chat-service",
                "created_at": time.time() - 3600,
                "progress": 100
            }
        ],
        "total": 1,
        "page": 1,
        "page_size": 20
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "test_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )