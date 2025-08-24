"""Azure IaC generator."""

import re
from typing import Any, Dict, List

from backend.models.schemas import (
    GeneratedResource,
    IaCFormat,
    IaCGenerationRequest,
    IaCProvider,
)

from .base import BaseGenerator


class AzureGenerator(BaseGenerator):
    """Generator for Azure infrastructure."""

    def __init__(self):
        """Initialize Azure generator."""
        super().__init__(IaCProvider.AZURE, IaCFormat.TERRAFORM)

    async def generate_infrastructure_code(
        self, request: IaCGenerationRequest, analysis: Dict[str, Any]
    ) -> str:
        """Generate Terraform code for Azure."""
        resource_group_config = self._get_resource_group_configuration(request)
        network_config = self._get_network_configuration(request, analysis)
        vm_config = self._get_vm_configuration(request, analysis)

        code = f"""terraform {{
  required_providers {{
    azurerm = {{
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }}
  }}
}}

provider "azurerm" {{
  features {{}}
}}

{resource_group_config}

{network_config}

{vm_config}
"""

        return code

    def _get_resource_group_configuration(self, request: IaCGenerationRequest) -> str:
        """Generate resource group configuration."""
        return f"""# Resource Group
resource "azurerm_resource_group" "main" {{
  name     = "rg-{request.project_name}-{request.environment}"
  location = var.location

  tags = var.common_tags
}}
"""

    def _get_network_configuration(
        self, request: IaCGenerationRequest, analysis: Dict[str, Any]
    ) -> str:
        """Generate network configuration."""
        return f"""# Virtual Network
resource "azurerm_virtual_network" "main" {{
  name                = "vnet-{request.project_name}"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  tags = var.common_tags
}}

# Subnet
resource "azurerm_subnet" "internal" {{
  name                 = "subnet-internal"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.2.0/24"]
}}

# Network Security Group
resource "azurerm_network_security_group" "main" {{
  name                = "nsg-{request.project_name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {{
    name                       = "SSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }}

  security_rule {{
    name                       = "HTTP"
    priority                   = 1002
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }}

  security_rule {{
    name                       = "HTTPS"
    priority                   = 1003
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }}

  tags = var.common_tags
}}
"""

    def _get_vm_configuration(
        self, request: IaCGenerationRequest, analysis: Dict[str, Any]
    ) -> str:
        """Generate VM configuration."""
        vm_size = self._determine_vm_size(analysis)

        return f"""# Public IP
resource "azurerm_public_ip" "main" {{
  name                = "pip-{request.project_name}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  allocation_method   = "Dynamic"

  tags = var.common_tags
}}

# Network Interface
resource "azurerm_network_interface" "main" {{
  name                = "nic-{request.project_name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {{
    name                          = "internal"
    subnet_id                     = azurerm_subnet.internal.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.main.id
  }}

  tags = var.common_tags
}}

# Associate Network Security Group to Network Interface
resource "azurerm_network_interface_security_group_association" "main" {{
  network_interface_id      = azurerm_network_interface.main.id
  network_security_group_id = azurerm_network_security_group.main.id
}}

# Virtual Machine
resource "azurerm_linux_virtual_machine" "main" {{
  name                = "vm-{request.project_name}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  size                = "{vm_size}"
  admin_username      = var.admin_username

  disable_password_authentication = true

  network_interface_ids = [
    azurerm_network_interface.main.id,
  ]

  admin_ssh_key {{
    username   = var.admin_username
    public_key = var.ssh_public_key
  }}

  os_disk {{
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
  }}

  source_image_reference {{
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }}

  tags = var.common_tags
}}
"""

    def _determine_vm_size(self, analysis: Dict[str, Any]) -> str:
        """Determine appropriate VM size."""
        complexity = analysis.get("estimated_complexity", 5)
        performance = analysis.get("performance", {})

        if performance.get("high_cpu", False) or complexity > 8:
            return "Standard_D2s_v3"
        elif performance.get("high_memory", False):
            return "Standard_E2s_v3"
        elif complexity > 5:
            return "Standard_B2s"
        else:
            return "Standard_B1s"

    async def generate_variables_file(self, request: IaCGenerationRequest) -> str:
        """Generate variables.tf file for Azure."""
        return f"""# Azure Configuration
variable "location" {{
  description = "Azure region"
  type        = string
  default     = "East US"
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

variable "common_tags" {{
  description = "Common tags for all resources"
  type        = map(string)
  default = {{
    Project     = "{request.project_name}"
    Environment = "{request.environment}"
    ManagedBy   = "terraform"
  }}
}}

# VM Configuration
variable "admin_username" {{
  description = "Admin username for the VM"
  type        = string
  default     = "azureuser"
}}

variable "ssh_public_key" {{
  description = "SSH public key for VM access"
  type        = string
}}
"""

    async def generate_outputs_file(self, request: IaCGenerationRequest) -> str:
        """Generate outputs.tf file for Azure."""
        return """# VM Information
output "vm_id" {{
  description = "ID of the created VM"
  value       = azurerm_linux_virtual_machine.main.id
}}

output "vm_name" {{
  description = "Name of the created VM"
  value       = azurerm_linux_virtual_machine.main.name
}}

output "public_ip_address" {{
  description = "Public IP address of the VM"
  value       = azurerm_public_ip.main.ip_address
}}

output "private_ip_address" {{
  description = "Private IP address of the VM"
  value       = azurerm_network_interface.main.private_ip_address
}}

output "ssh_connection" {{
  description = "SSH connection command"
  value       = "ssh ${{var.admin_username}}@${{azurerm_public_ip.main.ip_address}}"
}}

output "resource_group_name" {{
  description = "Name of the resource group"
  value       = azurerm_resource_group.main.name
}}

# Resource Summary
output "resource_summary" {{
  description = "Summary of created resources"
  value = {{
    project_name      = var.project_name
    environment       = var.environment
    location          = var.location
    vm_size           = azurerm_linux_virtual_machine.main.size
    vm_id             = azurerm_linux_virtual_machine.main.id
    resource_group    = azurerm_resource_group.main.name
  }}
}}
"""

    async def extract_resources(self, iac_code: str) -> List[GeneratedResource]:
        """Extract resources from Azure Terraform code."""
        resources = []

        # Find Azure resources
        resource_pattern = r'resource\s+"(azurerm_[^"]+)"\s+"([^"]+)"\s*\{'
        matches = re.finditer(resource_pattern, iac_code)

        for match in matches:
            resource_type = match.group(1)
            resource_name = match.group(2)

            resources.append(
                GeneratedResource(
                    name=resource_name,
                    type=resource_type,
                    provider=IaCProvider.AZURE,
                    configuration={},
                    dependencies=[],
                )
            )

        return resources

    async def estimate_costs(self, resources: List[GeneratedResource]) -> float:
        """Estimate costs for Azure resources."""
        # Basic cost estimation - would integrate with Azure Pricing API
        cost_map = {
            "azurerm_linux_virtual_machine": 15.0,  # Average monthly cost
            "azurerm_resource_group": 0.0,  # Resource groups are free
            "azurerm_virtual_network": 0.0,  # VNets are free
            "azurerm_subnet": 0.0,  # Subnets are free
            "azurerm_network_security_group": 0.0,  # NSGs are free
            "azurerm_public_ip": 3.0,  # Dynamic public IP cost
            "azurerm_network_interface": 0.0,  # NICs are free
        }

        total_cost = 0.0
        for resource in resources:
            resource_cost = cost_map.get(resource.type, 5.0)  # Default cost
            total_cost += resource_cost
            resource.estimated_monthly_cost = resource_cost

        return total_cost
