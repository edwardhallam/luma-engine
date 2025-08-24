"""Infrastructure as Code generation service."""

import json
import logging
import re
import subprocess  # nosec B404
import tempfile
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from backend.core.exceptions import AIDException
from backend.llm.service import LLMService
from backend.models.schemas import (
    CostEstimate,
    GeneratedResource,
    IaCFormat,
    IaCGenerationRequest,
    IaCGenerationResponse,
    IaCGenerationResult,
    IaCProvider,
    IaCValidationRequest,
    IaCValidationResponse,
    IaCValidationResult,
    ValidationIssue,
    ValidationSeverity,
)

logger = logging.getLogger(__name__)


class IaCGenerationService:
    """Service for generating Infrastructure as Code from requirements."""

    def __init__(self, llm_service: LLMService):
        """Initialize the IaC generation service."""
        self.llm_service = llm_service
        self.logger = logger.getChild(self.__class__.__name__)

    async def generate_iac(
        self, request: IaCGenerationRequest
    ) -> IaCGenerationResponse:
        """Generate Infrastructure as Code from requirements."""
        start_time = time.time()
        llm_calls = 0

        try:
            self.logger.info(
                f"Starting IaC generation for provider {request.provider} "
                f"in format {request.format}"
            )

            # Generate unique ID for this generation
            generation_id = str(uuid.uuid4())

            # Analyze requirements using LLM
            analysis_result, analysis_calls = await self._analyze_requirements(request)
            llm_calls += analysis_calls

            # Generate IaC code
            iac_result, generation_calls = await self._generate_iac_code(
                request, analysis_result, generation_id
            )
            llm_calls += generation_calls

            # Validate generated code if requested
            if request.enable_validation:
                validation_result = await self._validate_iac_code(
                    iac_result.iac_code, request.format, request.provider
                )
                iac_result.validation_result = validation_result
            else:
                iac_result.validation_result = IaCValidationResult(
                    valid=True,
                    syntax_valid=True,
                    security_valid=True,
                    total_issues=0,
                    error_count=0,
                    warning_count=0,
                )

            # Generate cost estimate if optimization is enabled
            if request.enable_optimization:
                cost_estimate = await self._estimate_costs(
                    iac_result.resources, request.provider
                )
                iac_result.cost_estimate = cost_estimate

            processing_time = time.time() - start_time
            iac_result.generation_time = processing_time

            return IaCGenerationResponse(
                success=True,
                result=iac_result,
                processing_time=processing_time,
                llm_calls=llm_calls,
            )

        except Exception as e:
            processing_time = time.time() - start_time
            self.logger.error(f"IaC generation failed: {e}", exc_info=True)

            return IaCGenerationResponse(
                success=False,
                error=str(e),
                error_details={"exception_type": type(e).__name__},
                processing_time=processing_time,
                llm_calls=llm_calls,
            )

    async def validate_iac(
        self, request: IaCValidationRequest
    ) -> IaCValidationResponse:
        """Validate Infrastructure as Code."""
        start_time = time.time()

        try:
            self.logger.info(f"Validating IaC in format {request.format}")

            validation_result = await self._validate_iac_code(
                request.iac_code, request.format, request.provider
            )

            cost_estimate = None
            if request.check_costs:
                # Parse resources from IaC code for cost estimation
                resources = await self._extract_resources_from_iac(
                    request.iac_code, request.format
                )
                cost_estimate = await self._estimate_costs(resources, request.provider)

            processing_time = time.time() - start_time

            return IaCValidationResponse(
                validation_result=validation_result,
                cost_estimate=cost_estimate,
                processing_time=processing_time,
            )

        except Exception as e:
            self.logger.error(f"IaC validation failed: {e}", exc_info=True)
            raise AIDException(
                message=f"Validation failed: {e}",
                details={"exception_type": type(e).__name__},
                status_code=500,
            )

    async def _analyze_requirements(
        self, request: IaCGenerationRequest
    ) -> Tuple[Dict[str, Any], int]:
        """Analyze natural language requirements."""
        prompt = f"""
        Analyze the following infrastructure requirements and extract structured information:

        Requirements: {request.requirements}
        Target Provider: {request.provider}
        Target Environment: {request.environment}
        Project: {request.project_name}

        Extract and return a JSON object with:
        - resources: List of infrastructure resources needed
        - networking: Networking requirements
        - security: Security requirements
        - performance: Performance requirements
        - storage: Storage requirements
        - estimated_complexity: Scale from 1-10

        Focus on {request.provider}-specific resources and configurations.
        """

        try:
            response = await self.llm_service.generate_response(prompt)
            analysis = json.loads(response)
            return analysis, 1
        except json.JSONDecodeError:
            # Fallback to basic analysis
            return {
                "resources": ["vm"],
                "networking": {"basic": True},
                "security": {"basic": True},
                "performance": {"basic": True},
                "storage": {"basic": True},
                "estimated_complexity": 5,
            }, 1

    async def _generate_iac_code(
        self,
        request: IaCGenerationRequest,
        analysis: Dict[str, Any],
        generation_id: str,
    ) -> Tuple[IaCGenerationResult, int]:
        """Generate IaC code from analyzed requirements."""
        llm_calls = 0

        # Generate main IaC code
        iac_code, calls = await self._generate_provider_specific_code(request, analysis)
        llm_calls += calls

        # Generate configuration files
        config_files = await self._generate_config_files(request, analysis)
        llm_calls += 1

        # Generate deployment scripts
        scripts = await self._generate_scripts(request, analysis)
        llm_calls += 1

        # Extract resources from generated code
        resources = await self._extract_resources_from_iac(iac_code, request.format)

        # Generate documentation
        readme = await self._generate_documentation(request, analysis, iac_code)
        llm_calls += 1

        deployment_instructions = await self._generate_deployment_instructions(
            request, iac_code
        )
        llm_calls += 1

        result = IaCGenerationResult(
            generation_id=generation_id,
            provider=request.provider,
            format=request.format,
            iac_code=iac_code,
            configuration_files=config_files,
            scripts=scripts,
            resources=resources,
            validation_result=IaCValidationResult(
                valid=True,
                syntax_valid=True,
                security_valid=True,
                total_issues=0,
                error_count=0,
                warning_count=0,
            ),
            readme=readme,
            deployment_instructions=deployment_instructions,
            template_used=request.template_id,
            requirements_analyzed=request.requirements,
            generation_time=0.0,  # Will be set by caller
            created_at=datetime.now(),
        )

        return result, llm_calls

    async def _generate_provider_specific_code(
        self, request: IaCGenerationRequest, analysis: Dict[str, Any]
    ) -> Tuple[str, int]:
        """Generate provider-specific IaC code."""
        provider_templates = {
            IaCProvider.PROXMOX: self._get_proxmox_template(),
            IaCProvider.AWS: self._get_aws_template(),
            IaCProvider.AZURE: self._get_azure_template(),
            IaCProvider.GCP: self._get_gcp_template(),
        }

        base_template = provider_templates.get(
            request.provider, provider_templates[IaCProvider.PROXMOX]
        )

        prompt = f"""
        Generate {request.format} code for {request.provider} based on:

        Requirements: {request.requirements}
        Analysis: {json.dumps(analysis, indent=2)}
        Project: {request.project_name}
        Environment: {request.environment}

        Base template to modify:
        {base_template}

        Generate complete, syntactically correct {request.format} code.
        Include proper resource naming, tags, and best practices.
        """

        if request.include_best_practices:
            prompt += "\nApply security and performance best practices."

        try:
            response = await self.llm_service.generate_response(prompt)
            # Clean up the response to extract just the code
            code = self._extract_code_from_response(response)
            return code, 1
        except Exception as e:
            self.logger.warning(f"Failed to generate code with LLM: {e}")
            return base_template, 1

    def _get_proxmox_template(self) -> str:
        """Get base Proxmox template."""
        return """
terraform {
  required_providers {
    proxmox = {
      source  = "telmate/proxmox"
      version = "2.9.14"
    }
  }
}

provider "proxmox" {
  pm_api_url      = var.pm_api_url
  pm_user         = var.pm_user
  pm_password     = var.pm_password
  pm_tls_insecure = true
}

variable "pm_api_url" {
  description = "Proxmox API URL"
  type        = string
}

variable "pm_user" {
  description = "Proxmox user"
  type        = string
}

variable "pm_password" {
  description = "Proxmox password"
  type        = string
  sensitive   = true
}

resource "proxmox_vm_qemu" "main" {
  name        = "vm-${var.project_name}"
  target_node = var.target_node
  clone       = var.template_name

  cores   = 2
  sockets = 1
  memory  = 2048

  disk {
    size    = "20G"
    type    = "scsi"
    storage = "local-lvm"
  }

  network {
    model  = "virtio"
    bridge = "vmbr0"
  }

  tags = "terraform,${var.environment}"
}

variable "project_name" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment"
  type        = string
  default     = "development"
}

variable "target_node" {
  description = "Proxmox node"
  type        = string
}

variable "template_name" {
  description = "VM template name"
  type        = string
  default     = "ubuntu-22.04-template"
}
"""

    def _get_aws_template(self) -> str:
        """Get base AWS template."""
        return """
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_instance" "main" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name        = "${var.project_name}-instance"
    Environment = var.environment
  }
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment"
  type        = string
  default     = "development"
}

variable "ami_id" {
  description = "AMI ID"
  type        = string
}

variable "instance_type" {
  description = "Instance type"
  type        = string
  default     = "t3.micro"
}
"""

    def _get_azure_template(self) -> str:
        """Get base Azure template."""
        return """
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "main" {
  name     = "rg-${var.project_name}"
  location = var.location
}

resource "azurerm_virtual_machine" "main" {
  name                = "vm-${var.project_name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  vm_size             = var.vm_size

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

variable "project_name" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment"
  type        = string
  default     = "development"
}

variable "location" {
  description = "Azure location"
  type        = string
  default     = "East US"
}

variable "vm_size" {
  description = "VM size"
  type        = string
  default     = "Standard_B1s"
}
"""

    def _get_gcp_template(self) -> str:
        """Get base GCP template."""
        return """
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_compute_instance" "main" {
  name         = "${var.project_name}-instance"
  machine_type = var.machine_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = var.image
    }
  }

  network_interface {
    network = "default"
  }

  labels = {
    environment = var.environment
    project     = var.project_name
  }
}

variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "project_name" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment"
  type        = string
  default     = "development"
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "GCP zone"
  type        = string
  default     = "us-central1-a"
}

variable "machine_type" {
  description = "Machine type"
  type        = string
  default     = "e2-micro"
}

variable "image" {
  description = "Boot disk image"
  type        = string
  default     = "debian-cloud/debian-11"
}
"""

    def _extract_code_from_response(self, response: str) -> str:
        """Extract code from LLM response."""
        # Look for code blocks
        code_blocks = re.findall(
            r"```(?:terraform|hcl)?\n(.*?)\n```", response, re.DOTALL
        )
        if code_blocks:
            return code_blocks[0].strip()

        # If no code blocks, return the whole response cleaned up
        return response.strip()

    async def _generate_config_files(
        self, request: IaCGenerationRequest, analysis: Dict[str, Any]
    ) -> Dict[str, str]:
        """Generate additional configuration files."""
        config_files = {}

        # Generate terraform.tfvars
        if request.format in [IaCFormat.TERRAFORM, IaCFormat.OPENTOFU]:
            tfvars = await self._generate_tfvars(request, analysis)
            config_files["terraform.tfvars.example"] = tfvars

        # Generate variables file
        variables = await self._generate_variables_file(request)
        config_files["variables.tf"] = variables

        return config_files

    async def _generate_tfvars(
        self, request: IaCGenerationRequest, analysis: Dict[str, Any]
    ) -> str:
        """Generate terraform.tfvars file."""
        tfvars = f"""# Terraform variables for {request.project_name}
project_name = "{request.project_name}"
environment  = "{request.environment}"

# Provider-specific variables
"""

        if request.provider == IaCProvider.PROXMOX:
            tfvars += """pm_api_url  = "https://your-proxmox-host:8006/api2/json"
pm_user     = "root@pam"
pm_password = "your-secure-password"  # pragma: allowlist secret
target_node = "your-proxmox-node"
"""
        elif request.provider == IaCProvider.AWS:
            tfvars += """aws_region    = "us-east-1"
ami_id        = "ami-0c55b159cbfafe1d0"
instance_type = "t3.micro"
"""

        return tfvars

    async def _generate_variables_file(self, request: IaCGenerationRequest) -> str:
        """Generate variables.tf file."""
        return f"""# Variables for {request.project_name}
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

variable "tags" {{
  description = "Common tags for all resources"
  type        = map(string)
  default     = {{
    Project     = "{request.project_name}"
    Environment = "{request.environment}"
    ManagedBy   = "terraform"
  }}
}}
"""

    async def _generate_scripts(
        self, request: IaCGenerationRequest, analysis: Dict[str, Any]
    ) -> Dict[str, str]:
        """Generate deployment scripts."""
        scripts = {}

        # Generate deployment script
        deploy_script = self._generate_deploy_script(request)
        scripts["deploy.sh"] = deploy_script

        # Generate cleanup script
        cleanup_script = self._generate_cleanup_script(request)
        scripts["cleanup.sh"] = cleanup_script

        return scripts

    def _generate_deploy_script(self, request: IaCGenerationRequest) -> str:
        """Generate deployment script."""
        return f"""#!/bin/bash
# Deployment script for {request.project_name}

set -e

echo "Deploying {request.project_name} infrastructure..."

# Initialize Terraform
terraform init

# Plan the deployment
terraform plan -var-file="terraform.tfvars"

# Apply the configuration
terraform apply -var-file="terraform.tfvars" -auto-approve

echo "Deployment completed successfully!"
"""

    def _generate_cleanup_script(self, request: IaCGenerationRequest) -> str:
        """Generate cleanup script."""
        return f"""#!/bin/bash
# Cleanup script for {request.project_name}

set -e

echo "Cleaning up {request.project_name} infrastructure..."

# Destroy the infrastructure
terraform destroy -var-file="terraform.tfvars" -auto-approve

echo "Cleanup completed successfully!"
"""

    async def _generate_documentation(
        self, request: IaCGenerationRequest, analysis: Dict[str, Any], iac_code: str
    ) -> str:
        """Generate README documentation."""
        return f"""# {request.project_name}

Infrastructure as Code for {request.project_name} using {request.format}.

## Requirements

{request.requirements}

## Generated Resources

This infrastructure creates the following resources on {request.provider}:

- Virtual machines/instances
- Networking components
- Storage resources
- Security configurations

## Prerequisites

1. {request.format} installed
2. Access to {request.provider} environment
3. Required credentials configured

## Deployment

1. Copy `terraform.tfvars.example` to `terraform.tfvars`
2. Update variables in `terraform.tfvars`
3. Run deployment script:

```bash
chmod +x deploy.sh
./deploy.sh
```

## Cleanup

To remove all resources:

```bash
chmod +x cleanup.sh
./cleanup.sh
```

## Generated by LumaEngine

This infrastructure was generated automatically from natural language requirements.
Environment: {request.environment}
Generated: {datetime.now().isoformat()}
"""

    async def _generate_deployment_instructions(
        self, request: IaCGenerationRequest, iac_code: str
    ) -> str:
        """Generate deployment instructions."""
        return f"""# Deployment Instructions

## Prerequisites

1. Install {request.format}
2. Configure {request.provider} credentials
3. Ensure network access to target environment

## Step-by-step Deployment

1. **Initialize**
   ```bash
   terraform init
   ```

2. **Configure Variables**
   Copy `terraform.tfvars.example` to `terraform.tfvars` and update values.

3. **Plan Deployment**
   ```bash
   terraform plan -var-file="terraform.tfvars"
   ```

4. **Deploy Infrastructure**
   ```bash
   terraform apply -var-file="terraform.tfvars"
   ```

## Verification

After deployment, verify resources are created properly in your {request.provider} console.

## Troubleshooting

Common issues and solutions:
- Check credentials are properly configured
- Ensure target environment has sufficient resources
- Verify network connectivity

Generated for project: {request.project_name}
Target provider: {request.provider}
Environment: {request.environment}
"""

    async def _validate_iac_code(
        self, iac_code: str, format: IaCFormat, provider: IaCProvider
    ) -> IaCValidationResult:
        """Validate IaC code syntax and best practices."""
        issues = []
        syntax_valid = True
        security_valid = True

        try:
            if format in [IaCFormat.TERRAFORM, IaCFormat.OPENTOFU]:
                validation_result = await self._validate_terraform(iac_code)
                issues.extend(validation_result)

                # Check if there are any syntax errors
                syntax_errors = [
                    issue
                    for issue in issues
                    if issue.severity == ValidationSeverity.ERROR
                ]
                syntax_valid = len(syntax_errors) == 0

            # Security validation
            security_issues = await self._validate_security(iac_code)
            issues.extend(security_issues)

            security_errors = [
                issue
                for issue in security_issues
                if issue.severity == ValidationSeverity.ERROR
            ]
            security_valid = len(security_errors) == 0

        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message=f"Validation error: {e}",
                    rule="internal_error",
                )
            )
            syntax_valid = False

        errors = [
            issue for issue in issues if issue.severity == ValidationSeverity.ERROR
        ]
        warnings = [
            issue for issue in issues if issue.severity == ValidationSeverity.WARNING
        ]
        info_issues = [
            issue for issue in issues if issue.severity == ValidationSeverity.INFO
        ]

        return IaCValidationResult(
            valid=syntax_valid and security_valid,
            syntax_valid=syntax_valid,
            security_valid=security_valid,
            errors=errors,
            warnings=warnings,
            info=info_issues,
            total_issues=len(issues),
            error_count=len(errors),
            warning_count=len(warnings),
        )

    async def _validate_terraform(self, iac_code: str) -> List[ValidationIssue]:
        """Validate Terraform syntax."""
        issues = []

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                tf_file = Path(temp_dir) / "main.tf"
                tf_file.write_text(iac_code)

                # Run terraform validate
                result = subprocess.run(  # nosec B603, B607
                    ["terraform", "init"],
                    cwd=temp_dir,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if result.returncode == 0:
                    result = subprocess.run(  # nosec B603, B607
                        ["terraform", "validate"],
                        cwd=temp_dir,
                        capture_output=True,
                        text=True,
                        timeout=30,
                    )

                    if result.returncode != 0:
                        issues.append(
                            ValidationIssue(
                                severity=ValidationSeverity.ERROR,
                                message=f"Terraform validation failed: {result.stderr}",
                                rule="terraform_validate",
                            )
                        )
                else:
                    issues.append(
                        ValidationIssue(
                            severity=ValidationSeverity.ERROR,
                            message=f"Terraform init failed: {result.stderr}",
                            rule="terraform_init",
                        )
                    )

        except subprocess.TimeoutExpired:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message="Terraform validation timed out",
                    rule="timeout",
                )
            )
        except FileNotFoundError:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message="Terraform not installed, skipping syntax validation",
                    rule="terraform_missing",
                )
            )
        except Exception as e:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message=f"Validation error: {e}",
                    rule="validation_error",
                )
            )

        return issues

    async def _validate_security(self, iac_code: str) -> List[ValidationIssue]:
        """Validate security best practices."""
        issues = []

        # Check for hardcoded secrets
        secret_patterns = [
            (r"password\s*=\s*[\"'][^\"']+[\"']", "Hardcoded password detected"),
            (r"api_key\s*=\s*[\"'][^\"']+[\"']", "Hardcoded API key detected"),
            (r"secret\s*=\s*[\"'][^\"']+[\"']", "Hardcoded secret detected"),
        ]

        for pattern, message in secret_patterns:
            matches = re.finditer(pattern, iac_code, re.IGNORECASE)
            for match in matches:
                line_num = iac_code[: match.start()].count("\n") + 1
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        message=message,
                        line=line_num,
                        rule="hardcoded_secrets",
                        suggestion="Use variables or secret management systems",
                    )
                )

        # Check for insecure configurations
        insecure_patterns = [
            (r"pm_tls_insecure\s*=\s*true", "TLS verification disabled"),
            (r"0\.0\.0\.0/0", "Overly permissive network access"),
        ]

        for pattern, message in insecure_patterns:
            matches = re.finditer(pattern, iac_code, re.IGNORECASE)
            for match in matches:
                line_num = iac_code[: match.start()].count("\n") + 1
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.WARNING,
                        message=message,
                        line=line_num,
                        rule="insecure_config",
                        suggestion="Review security implications",
                    )
                )

        return issues

    async def _extract_resources_from_iac(
        self, iac_code: str, format: IaCFormat
    ) -> List[GeneratedResource]:
        """Extract resource information from IaC code."""
        resources = []

        if format in [IaCFormat.TERRAFORM, IaCFormat.OPENTOFU]:
            # Parse Terraform resources
            resource_pattern = r'resource\s+"([^"]+)"\s+"([^"]+)"\s*\{'
            matches = re.finditer(resource_pattern, iac_code)

            for match in matches:
                resource_type = match.group(1)
                resource_name = match.group(2)

                resources.append(
                    GeneratedResource(
                        name=resource_name,
                        type=resource_type,
                        provider=IaCProvider.PROXMOX,  # Default, should be determined from context
                        configuration={},
                        dependencies=[],
                    )
                )

        return resources

    async def _estimate_costs(
        self, resources: List[GeneratedResource], provider: IaCProvider
    ) -> CostEstimate:
        """Estimate infrastructure costs."""
        # Basic cost estimation - would be enhanced with real pricing APIs
        base_costs = {
            IaCProvider.PROXMOX: {"vm": 0.0},  # Self-hosted, no direct costs
            IaCProvider.AWS: {"vm": 10.0, "storage": 0.10},
            IaCProvider.AZURE: {"vm": 12.0, "storage": 0.12},
            IaCProvider.GCP: {"vm": 8.0, "storage": 0.08},
        }

        provider_costs = base_costs.get(provider, {"vm": 10.0})

        total_cost = 0.0
        resource_costs = {}

        for resource in resources:
            cost = provider_costs.get("vm", 10.0)  # Default VM cost
            resource_costs[resource.name] = cost
            total_cost += cost

        return CostEstimate(
            monthly_cost=total_cost,
            annual_cost=total_cost * 12,
            compute_cost=total_cost,
            storage_cost=0.0,
            network_cost=0.0,
            other_cost=0.0,
            resource_costs=resource_costs,
            optimization_opportunities=[
                "Consider using spot instances for non-critical workloads",
                "Enable auto-scaling to optimize resource usage",
                "Use reserved instances for long-running workloads",
            ],
            potential_savings=total_cost * 0.3,  # Assume 30% potential savings
        )
