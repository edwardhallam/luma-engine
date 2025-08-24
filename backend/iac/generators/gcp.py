"""GCP IaC generator."""

import re
from typing import Any, Dict, List

from backend.models.schemas import (
    GeneratedResource,
    IaCFormat,
    IaCGenerationRequest,
    IaCProvider,
)

from .base import BaseGenerator


class GCPGenerator(BaseGenerator):
    """Generator for Google Cloud Platform infrastructure."""

    def __init__(self):
        """Initialize GCP generator."""
        super().__init__(IaCProvider.GCP, IaCFormat.TERRAFORM)

    async def generate_infrastructure_code(
        self, request: IaCGenerationRequest, analysis: Dict[str, Any]
    ) -> str:
        """Generate Terraform code for GCP."""
        network_config = self._get_network_configuration(request, analysis)
        instance_config = self._get_instance_configuration(request, analysis)
        firewall_config = self._get_firewall_configuration(request)

        code = f"""terraform {{
  required_providers {{
    google = {{
      source  = "hashicorp/google"
      version = "~> 4.0"
    }}
  }}
}}

provider "google" {{
  project = var.project_id
  region  = var.region
  zone    = var.zone
}}

{network_config}

{firewall_config}

{instance_config}
"""

        return code

    def _get_network_configuration(
        self, request: IaCGenerationRequest, analysis: Dict[str, Any]
    ) -> str:
        """Generate network configuration."""
        networking = analysis.get("networking", {})

        if networking.get("custom_network", False):
            return f"""# VPC Network
resource "google_compute_network" "vpc_network" {{
  name                    = "{request.project_name}-network"
  auto_create_subnetworks = false
}}

# Subnet
resource "google_compute_subnetwork" "subnet" {{
  name          = "{request.project_name}-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = var.region
  network       = google_compute_network.vpc_network.id
}}
"""
        else:
            return "# Using default network"

    def _get_firewall_configuration(self, request: IaCGenerationRequest) -> str:
        """Generate firewall configuration."""
        return f"""# Firewall rule for SSH
resource "google_compute_firewall" "ssh" {{
  name    = "{request.project_name}-allow-ssh"
  network = var.use_default_network ? "default" : google_compute_network.vpc_network.name

  allow {{
    protocol = "tcp"
    ports    = ["22"]
  }}

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["{request.project_name}"]
}}

# Firewall rule for HTTP
resource "google_compute_firewall" "http" {{
  name    = "{request.project_name}-allow-http"
  network = var.use_default_network ? "default" : google_compute_network.vpc_network.name

  allow {{
    protocol = "tcp"
    ports    = ["80", "443"]
  }}

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["{request.project_name}"]
}}
"""

    def _get_instance_configuration(
        self, request: IaCGenerationRequest, analysis: Dict[str, Any]
    ) -> str:
        """Generate compute instance configuration."""
        machine_type = self._determine_machine_type(analysis)
        disk_size = self._determine_disk_size(analysis)

        return f"""# Compute Instance
resource "google_compute_instance" "main" {{
  name         = "{request.project_name}-instance"
  machine_type = "{machine_type}"
  zone         = var.zone

  tags = ["{request.project_name}", var.environment]

  boot_disk {{
    initialize_params {{
      image = var.image
      size  = {disk_size}
      type  = "pd-standard"
    }}
  }}

  network_interface {{
    network    = var.use_default_network ? "default" : google_compute_network.vpc_network.name
    subnetwork = var.use_default_network ? null : google_compute_subnetwork.subnet.name

    access_config {{
      # Ephemeral public IP
    }}
  }}

  metadata = {{
    ssh-keys = "${{var.ssh_user}}:${{var.ssh_public_key}}"
  }}

  metadata_startup_script = var.startup_script

  service_account {{
    email  = var.service_account_email
    scopes = ["cloud-platform"]
  }}

  labels = {{
    project     = "{request.project_name}"
    environment = var.environment
    managed-by  = "terraform"
  }}
}}
"""

    def _determine_machine_type(self, analysis: Dict[str, Any]) -> str:
        """Determine appropriate machine type."""
        complexity = analysis.get("estimated_complexity", 5)
        performance = analysis.get("performance", {})

        if performance.get("high_cpu", False) or complexity > 8:
            return "n2-standard-2"
        elif performance.get("high_memory", False):
            return "n2-highmem-2"
        elif complexity > 5:
            return "e2-medium"
        else:
            return "e2-micro"

    def _determine_disk_size(self, analysis: Dict[str, Any]) -> int:
        """Determine disk size in GB."""
        storage = analysis.get("storage", {})

        if storage.get("large_storage", False):
            return 100
        elif storage.get("medium_storage", False):
            return 50
        else:
            return 20

    async def generate_variables_file(self, request: IaCGenerationRequest) -> str:
        """Generate variables.tf file for GCP."""
        return f"""# GCP Configuration
variable "project_id" {{
  description = "GCP Project ID"
  type        = string
}}

variable "region" {{
  description = "GCP region"
  type        = string
  default     = "us-central1"
}}

variable "zone" {{
  description = "GCP zone"
  type        = string
  default     = "us-central1-a"
}}

# Project Configuration
variable "project_name" {{
  description = "Name of the project"
  type        = string
  default     = "{request.project_name}"
}}

variable "environment" {{
  description = "Environment"
  type        = string
  default     = "{request.environment}"
}}

# Instance Configuration
variable "image" {{
  description = "Boot disk image"
  type        = string
  default     = "debian-cloud/debian-11"
}}

variable "ssh_user" {{
  description = "SSH username"
  type        = string
  default     = "gcp-user"
}}

variable "ssh_public_key" {{
  description = "SSH public key"
  type        = string
}}

variable "startup_script" {{
  description = "Startup script for the instance"
  type        = string
  default     = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y nginx
    systemctl start nginx
    systemctl enable nginx
    echo "<h1>Hello from {request.project_name}</h1>" > /var/www/html/index.html
  EOF
}}

variable "service_account_email" {{
  description = "Service account email"
  type        = string
  default     = null
}}

# Networking Configuration
variable "use_default_network" {{
  description = "Use default network instead of creating custom VPC"
  type        = bool
  default     = true
}}
"""

    async def generate_outputs_file(self, request: IaCGenerationRequest) -> str:
        """Generate outputs.tf file for GCP."""
        return """# Instance Information
output "instance_id" {{
  description = "ID of the compute instance"
  value       = google_compute_instance.main.id
}}

output "instance_name" {{
  description = "Name of the compute instance"
  value       = google_compute_instance.main.name
}}

output "instance_self_link" {{
  description = "Self-link of the compute instance"
  value       = google_compute_instance.main.self_link
}}

output "internal_ip" {{
  description = "Internal IP address of the instance"
  value       = google_compute_instance.main.network_interface[0].network_ip
}}

output "external_ip" {{
  description = "External IP address of the instance"
  value       = google_compute_instance.main.network_interface[0].access_config[0].nat_ip
}}

output "ssh_connection" {{
  description = "SSH connection command"
  value       = "gcloud compute ssh --zone=${{var.zone}} ${{var.ssh_user}}@${{google_compute_instance.main.name}} --project=${{var.project_id}}"
}}

# Network Information
output "network_name" {{
  description = "Name of the VPC network"
  value       = var.use_default_network ? "default" : google_compute_network.vpc_network.name
}}

output "subnet_name" {{
  description = "Name of the subnet"
  value       = var.use_default_network ? "default" : google_compute_subnetwork.subnet.name
}}

# Resource Summary
output "resource_summary" {{
  description = "Summary of created resources"
  value = {{
    project_id      = var.project_id
    project_name    = var.project_name
    environment     = var.environment
    region          = var.region
    zone            = var.zone
    machine_type    = google_compute_instance.main.machine_type
    instance_id     = google_compute_instance.main.id
    external_ip     = google_compute_instance.main.network_interface[0].access_config[0].nat_ip
  }}
}}
"""

    async def extract_resources(self, iac_code: str) -> List[GeneratedResource]:
        """Extract resources from GCP Terraform code."""
        resources = []

        # Find GCP resources
        resource_pattern = r'resource\s+"(google_[^"]+)"\s+"([^"]+)"\s*\{'
        matches = re.finditer(resource_pattern, iac_code)

        for match in matches:
            resource_type = match.group(1)
            resource_name = match.group(2)

            resources.append(
                GeneratedResource(
                    name=resource_name,
                    type=resource_type,
                    provider=IaCProvider.GCP,
                    configuration={},
                    dependencies=[],
                )
            )

        return resources

    async def estimate_costs(self, resources: List[GeneratedResource]) -> float:
        """Estimate costs for GCP resources."""
        # Basic cost estimation - would integrate with GCP Pricing API
        cost_map = {
            "google_compute_instance": 8.0,  # Average monthly cost
            "google_compute_network": 0.0,  # VPC networks are free
            "google_compute_subnetwork": 0.0,  # Subnets are free
            "google_compute_firewall": 0.0,  # Firewall rules are free
            "google_compute_address": 5.0,  # Static IP cost
        }

        total_cost = 0.0
        for resource in resources:
            resource_cost = cost_map.get(resource.type, 5.0)  # Default cost
            total_cost += resource_cost
            resource.estimated_monthly_cost = resource_cost

        return total_cost
