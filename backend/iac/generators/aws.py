"""AWS IaC generator."""

import re
from typing import Any, Dict, List

from backend.models.schemas import (
    GeneratedResource,
    IaCFormat,
    IaCGenerationRequest,
    IaCProvider,
)

from .base import BaseGenerator


class AWSGenerator(BaseGenerator):
    """Generator for AWS infrastructure."""

    def __init__(self):
        """Initialize AWS generator."""
        super().__init__(IaCProvider.AWS, IaCFormat.TERRAFORM)

    async def generate_infrastructure_code(
        self, request: IaCGenerationRequest, analysis: Dict[str, Any]
    ) -> str:
        """Generate Terraform code for AWS."""
        instance_config = self._get_instance_configuration(request, analysis)
        vpc_config = self._get_vpc_configuration(request, analysis)
        security_group_config = self._get_security_group_configuration(request)

        code = f"""terraform {{
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
  }}
}}

provider "aws" {{
  region = var.aws_region
}}

{vpc_config}

{security_group_config}

{instance_config}
"""

        return code

    def _get_vpc_configuration(
        self, request: IaCGenerationRequest, analysis: Dict[str, Any]
    ) -> str:
        """Generate VPC configuration."""
        networking = analysis.get("networking", {})

        if networking.get("custom_network", False):
            return f"""# VPC Configuration
resource "aws_vpc" "main" {{
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(var.common_tags, {{
    Name = "{request.project_name}-vpc"
  }})
}}

resource "aws_subnet" "public" {{
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidr
  availability_zone       = var.availability_zone
  map_public_ip_on_launch = true

  tags = merge(var.common_tags, {{
    Name = "{request.project_name}-public-subnet"
  }})
}}

resource "aws_internet_gateway" "main" {{
  vpc_id = aws_vpc.main.id

  tags = merge(var.common_tags, {{
    Name = "{request.project_name}-igw"
  }})
}}

resource "aws_route_table" "public" {{
  vpc_id = aws_vpc.main.id

  route {{
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }}

  tags = merge(var.common_tags, {{
    Name = "{request.project_name}-public-rt"
  }})
}}

resource "aws_route_table_association" "public" {{
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}}
"""
        else:
            return "# Using default VPC"

    def _get_security_group_configuration(self, request: IaCGenerationRequest) -> str:
        """Generate security group configuration."""
        return f"""# Security Group
resource "aws_security_group" "main" {{
  name_prefix = "{request.project_name}-"
  vpc_id      = var.use_default_vpc ? null : aws_vpc.main.id

  ingress {{
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }}

  ingress {{
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }}

  ingress {{
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }}

  egress {{
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }}

  tags = merge(var.common_tags, {{
    Name = "{request.project_name}-sg"
  }})
}}
"""

    def _get_instance_configuration(
        self, request: IaCGenerationRequest, analysis: Dict[str, Any]
    ) -> str:
        """Generate EC2 instance configuration."""
        instance_type = self._determine_instance_type(analysis)

        return f"""# EC2 Instance
resource "aws_instance" "main" {{
  ami                    = var.ami_id
  instance_type          = "{instance_type}"
  key_name              = var.key_pair_name
  vpc_security_group_ids = [aws_security_group.main.id]
  subnet_id             = var.use_default_vpc ? null : aws_subnet.public.id

  root_block_device {{
    volume_type = "gp3"
    volume_size = var.root_volume_size
    encrypted   = true
  }}

  tags = merge(var.common_tags, {{
    Name = "{request.project_name}-instance"
  }})
}}
"""

    def _determine_instance_type(self, analysis: Dict[str, Any]) -> str:
        """Determine appropriate instance type."""
        complexity = analysis.get("estimated_complexity", 5)
        performance = analysis.get("performance", {})

        if performance.get("high_cpu", False) or complexity > 8:
            return "c5.large"
        elif performance.get("high_memory", False):
            return "r5.large"
        elif complexity > 5:
            return "t3.medium"
        else:
            return "t3.micro"

    async def generate_variables_file(self, request: IaCGenerationRequest) -> str:
        """Generate variables.tf file for AWS."""
        return f"""# AWS Configuration
variable "aws_region" {{
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}}

variable "availability_zone" {{
  description = "Availability zone"
  type        = string
  default     = "us-east-1a"
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

# EC2 Configuration
variable "ami_id" {{
  description = "AMI ID for EC2 instance"
  type        = string
}}

variable "key_pair_name" {{
  description = "EC2 Key Pair name"
  type        = string
}}

variable "root_volume_size" {{
  description = "Root volume size in GB"
  type        = number
  default     = 20
}}

# Networking Configuration
variable "use_default_vpc" {{
  description = "Use default VPC instead of creating new one"
  type        = bool
  default     = true
}}

variable "vpc_cidr" {{
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}}

variable "public_subnet_cidr" {{
  description = "CIDR block for public subnet"
  type        = string
  default     = "10.0.1.0/24"
}}
"""

    async def generate_outputs_file(self, request: IaCGenerationRequest) -> str:
        """Generate outputs.tf file for AWS."""
        return """# Instance Information
output "instance_id" {{
  description = "ID of the EC2 instance"
  value       = aws_instance.main.id
}}

output "instance_public_ip" {{
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.main.public_ip
}}

output "instance_private_ip" {{
  description = "Private IP address of the EC2 instance"
  value       = aws_instance.main.private_ip
}}

output "instance_dns" {{
  description = "Public DNS name of the EC2 instance"
  value       = aws_instance.main.public_dns
}}

output "ssh_connection" {{
  description = "SSH connection command"
  value       = "ssh -i ${{var.key_pair_name}}.pem ubuntu@${{aws_instance.main.public_ip}}"
}}

# Resource Summary
output "resource_summary" {{
  description = "Summary of created resources"
  value = {{
    project_name    = var.project_name
    environment     = var.environment
    region          = var.aws_region
    instance_type   = aws_instance.main.instance_type
    instance_id     = aws_instance.main.id
    public_ip       = aws_instance.main.public_ip
  }}
}}
"""

    async def extract_resources(self, iac_code: str) -> List[GeneratedResource]:
        """Extract resources from AWS Terraform code."""
        resources = []

        # Find AWS resources
        resource_pattern = r'resource\s+"(aws_[^"]+)"\s+"([^"]+)"\s*\{'
        matches = re.finditer(resource_pattern, iac_code)

        for match in matches:
            resource_type = match.group(1)
            resource_name = match.group(2)

            resources.append(
                GeneratedResource(
                    name=resource_name,
                    type=resource_type,
                    provider=IaCProvider.AWS,
                    configuration={},
                    dependencies=[],
                )
            )

        return resources

    async def estimate_costs(self, resources: List[GeneratedResource]) -> float:
        """Estimate costs for AWS resources."""
        # Basic cost estimation - would integrate with AWS Pricing API
        cost_map = {
            "aws_instance": 10.0,  # Average monthly cost
            "aws_vpc": 0.0,  # VPCs are free
            "aws_security_group": 0.0,  # Security groups are free
            "aws_subnet": 0.0,  # Subnets are free
        }

        total_cost = 0.0
        for resource in resources:
            resource_cost = cost_map.get(resource.type, 5.0)  # Default cost
            total_cost += resource_cost
            resource.estimated_monthly_cost = resource_cost

        return total_cost
