"""Prompt template for requirement analysis."""

from langchain.prompts import PromptTemplate

REQUIREMENT_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["user_request", "available_templates", "resource_constraints"],
    template="""You are an expert infrastructure architect analyzing deployment requirements.

Your task is to parse the user's natural language request and output a structured deployment specification.

User Request:
{user_request}

Available Service Templates:
{available_templates}

Resource Constraints:
{resource_constraints}

Please analyze the request and provide a structured response in JSON format with the following schema:

{{
  "service_type": "string (e.g., 'chat-service', 'mcp-server', 'database', 'model-serving')",
  "service_name": "string (unique identifier for this deployment)",
  "description": "string (brief description of what this service does)",
  "template": "string (recommended template from available templates)",
  "resource_requirements": {{
    "cpu_cores": "number (estimated CPU cores needed)",
    "memory_gb": "number (estimated RAM in GB)",
    "storage_gb": "number (estimated storage in GB)",
    "gpu_required": "boolean (whether GPU is needed)",
    "gpu_memory_gb": "number (GPU memory if required)"
  }},
  "configuration": {{
    "environment_variables": {{}},
    "ports": [],
    "volumes": [],
    "networks": []
  }},
  "dependencies": [
    {{
      "service": "string (dependency service name)",
      "type": "string (e.g., 'database', 'cache', 'storage')",
      "required": "boolean"
    }}
  ],
  "scaling": {{
    "min_instances": "number",
    "max_instances": "number", 
    "auto_scaling": "boolean"
  }},
  "networking": {{
    "external_access": "boolean (needs internet access)",
    "load_balancer": "boolean (needs load balancing)",
    "ssl_required": "boolean (needs SSL/TLS)"
  }},
  "monitoring": {{
    "metrics_enabled": "boolean",
    "logging_level": "string (DEBUG, INFO, WARN, ERROR)",
    "health_check_path": "string (HTTP endpoint for health checks)"
  }},
  "backup": {{
    "enabled": "boolean",
    "frequency": "string (daily, weekly, monthly)",
    "retention_days": "number"
  }}
}}

Analysis Guidelines:
1. Extract the core service type from the user's request
2. Estimate resource requirements based on service complexity and expected load
3. Identify dependencies (databases, caches, external services)
4. Consider security requirements (SSL, network isolation)
5. Recommend appropriate monitoring and backup strategies
6. Select the most suitable template from available options
7. If the request is ambiguous, make reasonable assumptions and note them

Important Notes:
- For AI/ML services, consider GPU requirements
- For chat services, include database and session storage
- For MCP servers, consider tool-specific resource needs
- Always include health checks and monitoring
- Consider scalability from the start

Provide only the JSON response, no additional text or explanations."""
)


REQUIREMENT_REFINEMENT_PROMPT = PromptTemplate(
    input_variables=["original_spec", "user_feedback", "validation_errors"],
    template="""You are refining a deployment specification based on user feedback and validation results.

Original Specification:
{original_spec}

User Feedback:
{user_feedback}

Validation Errors (if any):
{validation_errors}

Please provide an updated JSON specification that addresses the feedback and resolves any validation errors.
Maintain the same JSON schema as the original specification.

Focus on:
1. Incorporating user corrections and preferences
2. Fixing any technical validation issues
3. Optimizing resource allocation based on feedback
4. Adjusting configuration parameters as requested

Provide only the updated JSON specification."""
)