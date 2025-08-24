"""Base generator class for Infrastructure as Code generation."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from backend.models.schemas import (
    GeneratedResource,
    IaCFormat,
    IaCGenerationRequest,
    IaCProvider,
)


class BaseGenerator(ABC):
    """Base class for IaC generators."""

    def __init__(self, provider: IaCProvider, format: IaCFormat):
        """Initialize the generator."""
        self.provider = provider
        self.format = format

    @abstractmethod
    async def generate_infrastructure_code(
        self, request: IaCGenerationRequest, analysis: Dict[str, Any]
    ) -> str:
        """Generate infrastructure code for the provider."""
        pass

    @abstractmethod
    async def generate_variables_file(self, request: IaCGenerationRequest) -> str:
        """Generate variables file for the provider."""
        pass

    @abstractmethod
    async def generate_outputs_file(self, request: IaCGenerationRequest) -> str:
        """Generate outputs file for the provider."""
        pass

    @abstractmethod
    async def extract_resources(self, iac_code: str) -> List[GeneratedResource]:
        """Extract resources from generated IaC code."""
        pass

    @abstractmethod
    async def estimate_costs(self, resources: List[GeneratedResource]) -> float:
        """Estimate costs for the generated resources."""
        pass

    def get_common_tags(self, request: IaCGenerationRequest) -> Dict[str, str]:
        """Get common tags for resources."""
        tags = {
            "Project": request.project_name,
            "Environment": request.environment,
            "ManagedBy": "lumaengine",
        }

        if request.tags:
            tags.update(request.tags)

        return tags

    def get_resource_name(
        self, request: IaCGenerationRequest, resource_type: str
    ) -> str:
        """Generate resource name following naming conventions."""
        return f"{request.project_name}-{resource_type}-{request.environment}"
