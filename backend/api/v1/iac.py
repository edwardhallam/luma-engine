"""Infrastructure as Code API endpoints."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from backend.core.exceptions import AIDException
from backend.iac.services import IaCGenerationService
from backend.llm.service import LLMService
from backend.models.schemas import (
    IaCGenerationRequest,
    IaCGenerationResponse,
    IaCValidationRequest,
    IaCValidationResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter()


def get_iac_generation_service() -> IaCGenerationService:
    """Dependency to get IaC generation service instance."""
    # Get LLM service - in production this would come from dependency injection
    llm_service = LLMService({})  # TODO: Get from config
    return IaCGenerationService(llm_service)


@router.post(
    "/generate",
    response_model=IaCGenerationResponse,
    summary="Generate Infrastructure as Code",
    description="Generate IaC from natural language requirements.",
)
async def generate_iac(
    request: IaCGenerationRequest,
    service: IaCGenerationService = Depends(get_iac_generation_service),
) -> IaCGenerationResponse:
    """Generate Infrastructure as Code from requirements."""
    try:
        logger.info(
            f"Generating IaC for provider {request.provider} "
            f"in format {request.format} for project {request.project_name}"
        )

        response = await service.generate_iac(request)

        if response.success:
            logger.info(
                f"IaC generation completed successfully in {response.processing_time:.2f}s"
            )
        else:
            logger.error(f"IaC generation failed: {response.error}")

        return response

    except AIDException as e:
        logger.error(f"IaC generation failed: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error during IaC generation: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during IaC generation",
        )


@router.post(
    "/validate",
    response_model=IaCValidationResponse,
    summary="Validate Infrastructure as Code",
    description="Validate IaC syntax, security, and best practices.",
)
async def validate_iac(
    request: IaCValidationRequest,
    service: IaCGenerationService = Depends(get_iac_generation_service),
) -> IaCValidationResponse:
    """Validate Infrastructure as Code."""
    try:
        logger.info(
            f"Validating IaC in format {request.format} for provider {request.provider}"
        )

        response = await service.validate_iac(request)

        if response.validation_result.valid:
            logger.info("IaC validation passed successfully")
        else:
            logger.warning(
                f"IaC validation found {response.validation_result.error_count} errors "
                f"and {response.validation_result.warning_count} warnings"
            )

        return response

    except AIDException as e:
        logger.error(f"IaC validation failed: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error during IaC validation: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during IaC validation",
        )


@router.get(
    "/providers",
    summary="List supported providers",
    description="Get list of supported IaC providers and formats.",
)
async def list_providers():
    """List supported IaC providers and formats."""
    try:
        return JSONResponse(
            content={
                "providers": [
                    {
                        "name": "proxmox",
                        "display_name": "Proxmox VE",
                        "description": "Proxmox Virtual Environment - Open-source virtualization platform",
                        "supported_formats": ["terraform", "opentofu"],
                        "cost_tier": "self-hosted",
                    },
                    {
                        "name": "aws",
                        "display_name": "Amazon Web Services",
                        "description": "Amazon Web Services cloud platform",
                        "supported_formats": ["terraform", "opentofu", "cdk"],
                        "cost_tier": "cloud",
                    },
                    {
                        "name": "azure",
                        "display_name": "Microsoft Azure",
                        "description": "Microsoft Azure cloud platform",
                        "supported_formats": ["terraform", "opentofu"],
                        "cost_tier": "cloud",
                    },
                    {
                        "name": "gcp",
                        "display_name": "Google Cloud Platform",
                        "description": "Google Cloud Platform",
                        "supported_formats": ["terraform", "opentofu"],
                        "cost_tier": "cloud",
                    },
                    {
                        "name": "digitalocean",
                        "display_name": "DigitalOcean",
                        "description": "DigitalOcean cloud platform",
                        "supported_formats": ["terraform"],
                        "cost_tier": "cloud-budget",
                    },
                    {
                        "name": "linode",
                        "display_name": "Linode",
                        "description": "Linode cloud platform",
                        "supported_formats": ["terraform"],
                        "cost_tier": "cloud-budget",
                    },
                    {
                        "name": "hetzner",
                        "display_name": "Hetzner Cloud",
                        "description": "Hetzner Cloud platform",
                        "supported_formats": ["terraform"],
                        "cost_tier": "cloud-budget",
                    },
                    {
                        "name": "vultr",
                        "display_name": "Vultr",
                        "description": "Vultr cloud platform",
                        "supported_formats": ["terraform"],
                        "cost_tier": "cloud-budget",
                    },
                ],
                "formats": [
                    {
                        "name": "terraform",
                        "display_name": "Terraform",
                        "description": "HashiCorp Terraform",
                        "file_extension": ".tf",
                    },
                    {
                        "name": "opentofu",
                        "display_name": "OpenTofu",
                        "description": "OpenTofu (Open Source Terraform fork)",
                        "file_extension": ".tf",
                    },
                    {
                        "name": "pulumi",
                        "display_name": "Pulumi",
                        "description": "Pulumi Infrastructure as Code",
                        "file_extension": ".py",
                    },
                    {
                        "name": "cdk",
                        "display_name": "AWS CDK",
                        "description": "AWS Cloud Development Kit",
                        "file_extension": ".ts",
                    },
                ],
            }
        )

    except Exception as e:
        logger.error(f"Error listing providers: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get(
    "/status",
    summary="Get IaC service status",
    description="Get the status of IaC generation services and dependencies.",
)
async def get_iac_status():
    """Get IaC service status."""
    try:
        # Check if required tools are available
        import shutil
        import subprocess  # nosec B404

        tool_status = {}

        # Check Terraform
        terraform_path = shutil.which("terraform")
        if terraform_path:
            try:
                result = subprocess.run(  # nosec B603, B607
                    ["terraform", "version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if result.returncode == 0:
                    version_line = result.stdout.split("\n")[0]
                    tool_status["terraform"] = {
                        "available": True,
                        "version": version_line,
                        "path": terraform_path,
                    }
                else:
                    tool_status["terraform"] = {
                        "available": False,
                        "error": "Failed to get version",
                    }
            except Exception as e:
                tool_status["terraform"] = {
                    "available": False,
                    "error": str(e),
                }
        else:
            tool_status["terraform"] = {
                "available": False,
                "error": "Not found in PATH",
            }

        # Check OpenTofu
        tofu_path = shutil.which("tofu")
        if tofu_path:
            try:
                result = subprocess.run(  # nosec B603, B607
                    ["tofu", "version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if result.returncode == 0:
                    version_line = result.stdout.split("\n")[0]
                    tool_status["opentofu"] = {
                        "available": True,
                        "version": version_line,
                        "path": tofu_path,
                    }
                else:
                    tool_status["opentofu"] = {
                        "available": False,
                        "error": "Failed to get version",
                    }
            except Exception as e:
                tool_status["opentofu"] = {
                    "available": False,
                    "error": str(e),
                }
        else:
            tool_status["opentofu"] = {
                "available": False,
                "error": "Not found in PATH",
            }

        return JSONResponse(
            content={
                "status": "healthy",
                "services": {
                    "iac_generation": "active",
                    "validation": "active",
                    "cost_estimation": "active",
                },
                "tools": tool_status,
                "supported_providers": 8,
                "supported_formats": 4,
            }
        )

    except Exception as e:
        logger.error(f"Error getting IaC status: {e}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "unhealthy",
                "error": str(e),
            },
        )


@router.get(
    "/examples",
    summary="Get example requests",
    description="Get example IaC generation requests for different scenarios.",
)
async def get_examples():
    """Get example IaC generation requests."""
    try:
        examples = {
            "simple_web_server": {
                "description": "Simple web server deployment",
                "request": {
                    "requirements": "I need a simple web server running Ubuntu with nginx installed, accessible from the internet with basic security.",
                    "provider": "proxmox",
                    "format": "terraform",
                    "project_name": "simple-web",
                    "environment": "development",
                    "enable_validation": True,
                    "enable_optimization": True,
                },
            },
            "database_server": {
                "description": "Database server with storage",
                "request": {
                    "requirements": "I need a PostgreSQL database server with 100GB storage, automated backups, and high availability setup.",
                    "provider": "aws",
                    "format": "terraform",
                    "project_name": "postgres-db",
                    "environment": "production",
                    "enable_validation": True,
                    "enable_optimization": True,
                },
            },
            "microservices_stack": {
                "description": "Microservices infrastructure",
                "request": {
                    "requirements": "I need a microservices setup with load balancer, 3 application servers, Redis cache, and monitoring stack.",
                    "provider": "azure",
                    "format": "terraform",
                    "project_name": "microservices",
                    "environment": "staging",
                    "enable_validation": True,
                    "enable_optimization": True,
                },
            },
            "development_environment": {
                "description": "Development environment",
                "request": {
                    "requirements": "Create a development environment with GitLab, Jenkins CI/CD, and artifact storage.",
                    "provider": "gcp",
                    "format": "terraform",
                    "project_name": "dev-env",
                    "environment": "development",
                    "enable_validation": True,
                    "enable_optimization": False,
                },
            },
        }

        return JSONResponse(content={"examples": examples})

    except Exception as e:
        logger.error(f"Error getting examples: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
