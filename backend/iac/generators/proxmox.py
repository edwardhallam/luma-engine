"""Proxmox IaC generator."""

import re
from typing import Any, Dict, List

from backend.models.schemas import (
    GeneratedResource,
    IaCFormat,
    IaCGenerationRequest,
    IaCProvider,
)

from .base import BaseGenerator


class ProxmoxGenerator(BaseGenerator):
    """Generator for Proxmox infrastructure."""

    def __init__(self):
        """Initialize Proxmox generator."""
        super().__init__(IaCProvider.PROXMOX, IaCFormat.TERRAFORM)

    async def generate_infrastructure_code(
        self, request: IaCGenerationRequest, analysis: Dict[str, Any]
    ) -> str:
        """Generate Terraform code for Proxmox."""
        vm_config = self._get_vm_configuration(request, analysis)
        networking_config = self._get_networking_configuration(analysis)
        storage_config = self._get_storage_configuration(analysis)

        code = f"""terraform {{
  required_providers {{
    proxmox = {{
      source  = "telmate/proxmox"
      version = "2.9.14"
    }}
  }}
}}

provider "proxmox" {{
  pm_api_url      = var.pm_api_url
  pm_user         = var.pm_user
  pm_password     = var.pm_password
  pm_tls_insecure = var.pm_tls_insecure
}}

{vm_config}

{networking_config}

{storage_config}
"""

        return code

    def _get_vm_configuration(
        self, request: IaCGenerationRequest, analysis: Dict[str, Any]
    ) -> str:
        """Generate VM configuration."""
        vm_name = self.get_resource_name(request, "vm")
        tags = self.get_common_tags(request)
        tag_string = ",".join([f"{k}={v}" for k, v in tags.items()])

        # Determine VM specifications based on analysis
        cores = self._determine_cores(analysis)
        memory = self._determine_memory(analysis)
        disk_size = self._determine_disk_size(analysis)

        return f"""resource "proxmox_vm_qemu" "main" {{
  name        = "{vm_name}"
  target_node = var.target_node
  clone       = var.template_name

  # CPU and Memory
  cores   = {cores}
  sockets = 1
  memory  = {memory}

  # Boot and storage
  boot = "c"
  bootdisk = "scsi0"

  disk {{
    size    = "{disk_size}G"
    type    = "scsi"
    storage = var.storage_pool
  }}

  # Networking
  network {{
    model  = "virtio"
    bridge = var.network_bridge
  }}

  # Cloud-init configuration
  os_type = "cloud-init"

  # Tags
  tags = "{tag_string}"

  lifecycle {{
    create_before_destroy = true
  }}
}}"""

    def _get_networking_configuration(self, analysis: Dict[str, Any]) -> str:
        """Generate networking configuration if needed."""
        networking = analysis.get("networking", {})

        if networking.get("custom_network", False):
            return """
# Custom networking configuration
resource "proxmox_vm_qemu" "load_balancer" {
  count       = var.enable_load_balancer ? 1 : 0
  name        = "${var.project_name}-lb-${var.environment}"
  target_node = var.target_node
  clone       = var.template_name

  cores   = 1
  memory  = 1024

  disk {
    size    = "10G"
    type    = "scsi"
    storage = var.storage_pool
  }

  network {
    model  = "virtio"
    bridge = var.network_bridge
  }

  tags = "load-balancer,${var.environment}"
}
"""
        return "# Using default networking configuration"

    def _get_storage_configuration(self, analysis: Dict[str, Any]) -> str:
        """Generate storage configuration if needed."""
        storage = analysis.get("storage", {})

        if storage.get("additional_storage", False):
            return """
# Additional storage disk
resource "proxmox_vm_qemu" "storage_vm" {
  count       = var.enable_additional_storage ? 1 : 0
  name        = "${var.project_name}-storage-${var.environment}"
  target_node = var.target_node
  clone       = var.template_name

  cores   = 2
  memory  = 4096

  disk {
    size    = "20G"
    type    = "scsi"
    storage = var.storage_pool
  }

  disk {
    size    = "100G"
    type    = "scsi"
    storage = var.storage_pool
  }

  network {
    model  = "virtio"
    bridge = var.network_bridge
  }

  tags = "storage,${var.environment}"
}
"""
        return "# Using default storage configuration"

    def _determine_cores(self, analysis: Dict[str, Any]) -> int:
        """Determine number of CPU cores needed."""
        complexity = analysis.get("estimated_complexity", 5)
        performance = analysis.get("performance", {})

        if performance.get("high_cpu", False) or complexity > 8:
            return 4
        elif complexity > 5:
            return 2
        else:
            return 1

    def _determine_memory(self, analysis: Dict[str, Any]) -> int:
        """Determine memory allocation in MB."""
        complexity = analysis.get("estimated_complexity", 5)
        performance = analysis.get("performance", {})

        if performance.get("high_memory", False) or complexity > 8:
            return 8192  # 8GB
        elif complexity > 5:
            return 4096  # 4GB
        else:
            return 2048  # 2GB

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
        """Generate variables.tf file for Proxmox."""
        return f"""# Proxmox connection variables
variable "pm_api_url" {{
  description = "Proxmox API URL"
  type        = string
}}

variable "pm_user" {{
  description = "Proxmox user"
  type        = string
  default     = "root@pam"
}}

variable "pm_password" {{
  description = "Proxmox password"
  type        = string
  sensitive   = true
}}

variable "pm_tls_insecure" {{
  description = "Allow insecure TLS connections"
  type        = bool
  default     = true
}}

# Infrastructure variables
variable "project_name" {{
  description = "Name of the project"
  type        = string
  default     = "{request.project_name}"
}}

variable "environment" {{
  description = "Environment (development, staging, production)"
  type        = string
  default     = "{request.environment}"
}}

variable "target_node" {{
  description = "Proxmox node to deploy to"
  type        = string
}}

variable "template_name" {{
  description = "VM template name"
  type        = string
  default     = "ubuntu-22.04-template"
}}

variable "storage_pool" {{
  description = "Storage pool for VM disks"
  type        = string
  default     = "local-lvm"
}}

variable "network_bridge" {{
  description = "Network bridge for VMs"
  type        = string
  default     = "vmbr0"
}}

# Optional features
variable "enable_load_balancer" {{
  description = "Enable load balancer VM"
  type        = bool
  default     = false
}}

variable "enable_additional_storage" {{
  description = "Enable additional storage VM"
  type        = bool
  default     = false
}}
"""

    async def generate_outputs_file(self, request: IaCGenerationRequest) -> str:
        """Generate outputs.tf file for Proxmox."""
        return """# VM information
output "vm_id" {{
  description = "ID of the created VM"
  value       = proxmox_vm_qemu.main.vmid
}}

output "vm_name" {{
  description = "Name of the created VM"
  value       = proxmox_vm_qemu.main.name
}}

output "vm_ip_address" {{
  description = "IP address of the VM"
  value       = proxmox_vm_qemu.main.default_ipv4_address
}}

output "vm_ssh_host" {{
  description = "SSH connection string"
  value       = "${{proxmox_vm_qemu.main.ssh_user}}@${{proxmox_vm_qemu.main.default_ipv4_address}}"
}}

# Resource information
output "resource_summary" {{
  description = "Summary of created resources"
  value = {{
    project_name = var.project_name
    environment  = var.environment
    vm_cores     = proxmox_vm_qemu.main.cores
    vm_memory    = proxmox_vm_qemu.main.memory
    vm_storage   = proxmox_vm_qemu.main.disk[0].size
  }}
}}
"""

    async def extract_resources(self, iac_code: str) -> List[GeneratedResource]:
        """Extract resources from Proxmox Terraform code."""
        resources = []

        # Find VM resources
        vm_pattern = r'resource\s+"proxmox_vm_qemu"\s+"([^"]+)"\s*\{'
        vm_matches = re.finditer(vm_pattern, iac_code)

        for match in vm_matches:
            resource_name = match.group(1)

            # Extract configuration details
            config = self._extract_vm_config(iac_code, match.start(), match.end())

            resources.append(
                GeneratedResource(
                    name=resource_name,
                    type="proxmox_vm_qemu",
                    provider=IaCProvider.PROXMOX,
                    configuration=config,
                    dependencies=[],
                    estimated_monthly_cost=0.0,  # Proxmox is self-hosted
                )
            )

        return resources

    def _extract_vm_config(self, iac_code: str, start: int, end: int) -> Dict[str, Any]:
        """Extract VM configuration from code block."""
        # This is a simplified extraction - would be enhanced with proper HCL parsing
        config = {}

        # Extract basic properties
        if "cores" in iac_code[start:end]:
            cores_match = re.search(r"cores\s*=\s*(\d+)", iac_code[start:end])
            if cores_match:
                config["cores"] = int(cores_match.group(1))

        if "memory" in iac_code[start:end]:
            memory_match = re.search(r"memory\s*=\s*(\d+)", iac_code[start:end])
            if memory_match:
                config["memory"] = int(memory_match.group(1))

        return config

    async def estimate_costs(self, resources: List[GeneratedResource]) -> float:
        """Estimate costs for Proxmox resources."""
        # Proxmox is self-hosted, so direct cloud costs are $0
        # Could include electricity/hardware depreciation costs if needed
        return 0.0
