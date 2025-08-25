"""Template service for managing infrastructure templates."""

import logging
from datetime import datetime
from typing import List, Optional

from backend.models.schemas import (
    Template,
    TemplateCategory,
    TemplateListResponse,
    TemplateParameter,
    TemplateRequest,
    TemplateResource,
    TemplateResponse,
    TemplateStatus,
    TemplateUsageStats,
    TemplateValidation,
    TemplateValidationRequest,
    TemplateValidationResponse,
)

logger = logging.getLogger(__name__)


class TemplateService:
    """Service for managing infrastructure templates."""

    def __init__(self):
        """Initialize template service."""
        # Create proper Template objects with all required fields
        now = datetime.utcnow()

        self._mock_templates = [
            Template(
                template_id="homelab-basic",
                name="Basic Homelab Setup",
                description="Essential services for a homelab environment including Proxmox configuration, Docker setup, and basic networking",
                category=TemplateCategory.HOMELAB,
                status=TemplateStatus.ACTIVE,
                parameters=[
                    TemplateParameter(
                        name="vm_count",
                        type="number",
                        description="Number of VMs to create",
                        default_value=3,
                        min_value=1,
                        max_value=10,
                    ),
                    TemplateParameter(
                        name="cpu_cores",
                        type="number",
                        description="CPU cores per VM",
                        default_value=2,
                        min_value=1,
                        max_value=8,
                    ),
                ],
                resources=[
                    TemplateResource(
                        type="vm",
                        name="docker-host",
                        configuration={"memory": "4GB", "storage": "50GB", "cpu": 2},
                        dependencies=[],
                    )
                ],
                validation=TemplateValidation(),
                iac_template='# Proxmox VM Template\nresource "proxmox_vm_qemu" "docker_host" {\n  # Configuration here\n}',
                version="1.0.0",
                author="LumaEngine Team",
                tags=["proxmox", "docker", "basic", "homelab"],
                created_at=now,
                updated_at=now,
            ),
            Template(
                template_id="k8s-cluster",
                name="Kubernetes Cluster",
                description="Production-ready Kubernetes cluster setup with high availability and monitoring",
                category=TemplateCategory.ORCHESTRATION,
                status=TemplateStatus.ACTIVE,
                parameters=[
                    TemplateParameter(
                        name="node_count",
                        type="number",
                        description="Number of worker nodes",
                        default_value=3,
                        min_value=1,
                        max_value=20,
                    )
                ],
                resources=[
                    TemplateResource(
                        type="vm",
                        name="k8s-master",
                        configuration={"memory": "8GB", "storage": "100GB", "cpu": 4},
                        dependencies=[],
                    )
                ],
                validation=TemplateValidation(),
                iac_template='# Kubernetes Cluster Template\nresource "proxmox_vm_qemu" "k8s_master" {\n  # K8s master configuration\n}',
                version="1.2.0",
                author="LumaEngine Team",
                tags=["kubernetes", "k8s", "cluster", "orchestration"],
                min_cpu=4.0,
                min_memory_gb=8.0,
                min_storage_gb=100.0,
                created_at=now,
                updated_at=now,
            ),
            Template(
                template_id="monitoring-stack",
                name="Monitoring & Observability",
                description="Complete monitoring stack with Prometheus, Grafana, Jaeger, and alerting",
                category=TemplateCategory.MONITORING,
                status=TemplateStatus.ACTIVE,
                parameters=[
                    TemplateParameter(
                        name="retention_days",
                        type="number",
                        description="Data retention in days",
                        default_value=30,
                        min_value=7,
                        max_value=365,
                    )
                ],
                resources=[
                    TemplateResource(
                        type="container",
                        name="prometheus",
                        configuration={
                            "image": "prom/prometheus:latest",
                            "ports": [9090],
                        },
                        dependencies=[],
                    ),
                    TemplateResource(
                        type="container",
                        name="grafana",
                        configuration={
                            "image": "grafana/grafana:latest",
                            "ports": [3000],
                        },
                        dependencies=["prometheus"],
                    ),
                ],
                validation=TemplateValidation(),
                iac_template='# Monitoring Stack Template\nresource "docker_container" "prometheus" {\n  # Prometheus configuration\n}',
                version="2.0.1",
                author="LumaEngine Team",
                tags=["prometheus", "grafana", "jaeger", "monitoring", "observability"],
                min_cpu=2.0,
                min_memory_gb=4.0,
                min_storage_gb=50.0,
                created_at=now,
                updated_at=now,
            ),
        ]

    async def list_templates(
        self,
        page: int = 1,
        page_size: int = 20,
        category: Optional[TemplateCategory] = None,
        status: Optional[TemplateStatus] = None,
        search: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> TemplateListResponse:
        """List templates with optional filtering."""
        filtered_templates = self._mock_templates.copy()

        # Apply filters
        if category:
            filtered_templates = [
                t for t in filtered_templates if t.category == category
            ]

        if status:
            filtered_templates = [t for t in filtered_templates if t.status == status]

        if search:
            search_lower = search.lower()
            filtered_templates = [
                t
                for t in filtered_templates
                if search_lower in t.name.lower()
                or search_lower in t.description.lower()
            ]

        if tags:
            filtered_templates = [
                t for t in filtered_templates if any(tag in t.tags for tag in tags)
            ]

        # Pagination
        start = (page - 1) * page_size
        end = start + page_size
        paginated_templates = filtered_templates[start:end]

        return TemplateListResponse(
            templates=paginated_templates,
            total=len(filtered_templates),
            page=page,
            page_size=page_size,
            total_pages=(len(filtered_templates) + page_size - 1) // page_size,
        )

    async def get_template(
        self, template_id: str, include_preview: bool = False
    ) -> Optional[TemplateResponse]:
        """Get template by ID."""
        template = next(
            (t for t in self._mock_templates if t.template_id == template_id), None
        )

        if not template:
            return None

        preview_data = None

        if include_preview:
            preview_data = {
                "estimated_cost": "$15-25/month",
                "estimated_deployment_time": "15-20 minutes",
                "resources": {
                    "cpu_cores": int(template.min_cpu),
                    "memory_gb": int(template.min_memory_gb),
                    "storage_gb": int(template.min_storage_gb),
                    "network_ports": [80, 443, 22],
                },
            }

        return TemplateResponse(
            template=template,
            deployment_preview=preview_data,
        )

    async def create_template(self, request: TemplateRequest) -> TemplateResponse:
        """Create a new template."""
        # Mock implementation - would normally save to database
        new_template_data = {
            "id": f"custom-{len(self._mock_templates) + 1}",
            "name": request.name,
            "description": request.description,
            "category": request.category,
            "status": TemplateStatus.DRAFT,
            "tags": request.tags or [],
            "version": "1.0.0",
            "rating": 0.0,
            "downloads": 0,
        }

        self._mock_templates.append(new_template_data)
        template = Template(**new_template_data)

        return TemplateResponse(template=template)

    async def update_template(
        self, template_id: str, request: TemplateRequest
    ) -> TemplateResponse:
        """Update an existing template."""
        # Mock implementation
        template_data = next(
            (t for t in self._mock_templates if t["id"] == template_id), None
        )

        if not template_data:
            raise ValueError(f"Template {template_id} not found")

        # Update fields
        template_data.update(
            {
                "name": request.name,
                "description": request.description,
                "category": request.category,
                "tags": request.tags or [],
            }
        )

        template = Template(**template_data)
        return TemplateResponse(template=template)

    async def delete_template(self, template_id: str, force: bool = False) -> None:
        """Delete a template."""
        # Mock implementation
        self._mock_templates = [
            t for t in self._mock_templates if t["id"] != template_id
        ]

    async def validate_template(
        self, request: TemplateValidationRequest
    ) -> TemplateValidationResponse:
        """Validate a template."""
        # Mock validation - always returns success
        return TemplateValidationResponse(
            is_valid=True,
            errors=[],
            warnings=["This is a mock validation - implement real validation"],
            recommendations=["Consider adding resource limits", "Add health checks"],
        )

    async def import_template(
        self, content: bytes, filename: Optional[str]
    ) -> TemplateResponse:
        """Import a template from file content."""
        # Mock implementation
        new_template_data = {
            "id": f"imported-{len(self._mock_templates) + 1}",
            "name": f"Imported Template ({filename})",
            "description": "Template imported from file",
            "category": TemplateCategory.CUSTOM,
            "status": TemplateStatus.DRAFT,
            "tags": ["imported"],
            "version": "1.0.0",
            "rating": 0.0,
            "downloads": 0,
        }

        self._mock_templates.append(new_template_data)
        template = Template(**new_template_data)

        return TemplateResponse(template=template)

    async def export_template(self, template_id: str, format: str):
        """Export a template."""
        template_data = next(
            (t for t in self._mock_templates if t["id"] == template_id), None
        )

        if not template_data:
            raise ValueError(f"Template {template_id} not found")

        if format == "json":
            return template_data
        else:
            return {"message": f"Export format {format} not implemented yet"}

    async def get_template_usage(self, template_id: str) -> TemplateUsageStats:
        """Get usage statistics for a template."""
        return TemplateUsageStats(
            template_id=template_id,
            total_deployments=42,
            active_deployments=15,
            successful_deployments=38,
            failed_deployments=4,
            average_deployment_time=18.5,
            last_used="2025-08-24T18:00:00Z",
        )

    async def clone_template(self, template_id: str, new_name: str) -> TemplateResponse:
        """Clone an existing template."""
        template_data = next(
            (t for t in self._mock_templates if t["id"] == template_id), None
        )

        if not template_data:
            raise ValueError(f"Template {template_id} not found")

        # Create clone
        cloned_data = template_data.copy()
        cloned_data.update(
            {
                "id": f"clone-{len(self._mock_templates) + 1}",
                "name": new_name,
                "status": TemplateStatus.DRAFT,
                "version": "1.0.0",
                "downloads": 0,
            }
        )

        self._mock_templates.append(cloned_data)
        template = Template(**cloned_data)

        return TemplateResponse(template=template)

    async def get_template_categories(self) -> List[str]:
        """Get all available template categories."""
        return [category.value for category in TemplateCategory]

    async def search_templates(
        self,
        query: str,
        category: Optional[TemplateCategory] = None,
        min_rating: Optional[float] = None,
    ) -> TemplateListResponse:
        """Search templates."""
        filtered_templates = self._mock_templates.copy()

        # Search in name and description
        query_lower = query.lower()
        filtered_templates = [
            t
            for t in filtered_templates
            if query_lower in t["name"].lower()
            or query_lower in t["description"].lower()
        ]

        # Apply additional filters
        if category:
            filtered_templates = [
                t for t in filtered_templates if t["category"] == category
            ]

        if min_rating:
            filtered_templates = [
                t for t in filtered_templates if t["rating"] >= min_rating
            ]

        return TemplateListResponse(
            templates=[Template(**t) for t in filtered_templates],
            total=len(filtered_templates),
            page=1,
            page_size=len(filtered_templates),
            total_pages=1,
        )

    async def get_recommended_templates(
        self, limit: int = 10, user_context: Optional[str] = None
    ) -> List[Template]:
        """Get recommended templates."""
        # Mock recommendations - return templates sorted by rating and downloads
        sorted_templates = sorted(
            self._mock_templates,
            key=lambda t: (t["rating"], t["downloads"]),
            reverse=True,
        )

        return [Template(**t) for t in sorted_templates[:limit]]
