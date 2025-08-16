"""Prompt template for Infrastructure as Code generation."""

from langchain.prompts import PromptTemplate

IAC_GENERATION_PROMPT = PromptTemplate(
    input_variables=["deployment_spec", "template_base", "target_platform", "existing_resources"],
    template="""You are an expert DevOps engineer generating Infrastructure as Code configurations.

Your task is to generate OpenTofu/Terraform configuration files based on the deployment specification.

Deployment Specification:
{deployment_spec}

Base Template:
{template_base}

Target Platform: {target_platform}

Existing Resources:
{existing_resources}

Generate a complete OpenTofu configuration with the following structure:

1. **main.tf** - Main resource definitions
2. **variables.tf** - Input variables
3. **outputs.tf** - Output values
4. **versions.tf** - Provider versions and requirements

Requirements:
- Use Proxmox provider for VM/LXC provisioning
- Include proper resource dependencies
- Add appropriate tags and labels
- Configure networking (VLANs, firewall rules)
- Set up storage volumes as needed
- Include cloud-init configuration for VMs
- Add monitoring and logging setup

For each file, provide the content in this format:

```hcl
# filename: main.tf
[content here]
```

```hcl
# filename: variables.tf
[content here]
```

Key Considerations:
1. **Security**: Use least privilege access, secure defaults
2. **Scalability**: Design for horizontal scaling where applicable
3. **Monitoring**: Include health checks and metrics endpoints
4. **Backup**: Configure automated backup schedules
5. **Networking**: Proper VLAN isolation and firewall rules
6. **Storage**: Appropriate storage types and sizes
7. **High Availability**: Consider redundancy for critical services

Platform-Specific Guidelines:

**Proxmox**:
- Use appropriate VM templates (Ubuntu 22.04 LTS recommended)
- Configure CPU/memory based on requirements
- Set up networking with proper VLANs
- Use cloud-init for initial configuration
- Configure storage on appropriate storage pools

**Kubernetes** (if applicable):
- Use proper namespaces for isolation
- Set resource limits and requests
- Configure ingress controllers
- Add persistent volume claims for stateful services
- Include service monitors for Prometheus

Generate production-ready, well-documented infrastructure code that follows best practices."""
)

IAC_VALIDATION_PROMPT = PromptTemplate(
    input_variables=["iac_config", "validation_errors", "security_findings"],
    template="""You are reviewing and fixing Infrastructure as Code configuration.

IaC Configuration:
{iac_config}

Validation Errors:
{validation_errors}

Security Findings:
{security_findings}

Please provide corrected configuration files that address all issues:

1. Fix syntax and validation errors
2. Resolve security vulnerabilities
3. Optimize resource configurations
4. Ensure best practices compliance

For each corrected file, use this format:

```hcl
# filename: [filename]
[corrected content]
```

Focus on:
- Proper syntax and structure
- Security hardening
- Resource optimization
- Dependency management
- Error handling"""
)

IAC_OPTIMIZATION_PROMPT = PromptTemplate(
    input_variables=["current_config", "performance_metrics", "cost_analysis"],
    template="""You are optimizing Infrastructure as Code for performance and cost.

Current Configuration:
{current_config}

Performance Metrics:
{performance_metrics}

Cost Analysis:
{cost_analysis}

Provide optimized configuration that:
1. Improves performance based on metrics
2. Reduces costs where possible
3. Maintains reliability and security
4. Implements auto-scaling where beneficial

Show the optimized files with explanations for major changes."""
)