"""Prompt template for error diagnosis and resolution."""

from langchain.prompts import PromptTemplate

ERROR_DIAGNOSIS_PROMPT = PromptTemplate(
    input_variables=["error_logs", "deployment_config", "system_state", "previous_fixes"],
    template="""You are an expert DevOps troubleshooter analyzing deployment failures.

Your task is to diagnose the error, categorize it, and provide actionable solutions.

Error Logs:
{error_logs}

Deployment Configuration:
{deployment_config}

System State:
{system_state}

Previous Fix Attempts:
{previous_fixes}

Please provide a structured analysis in JSON format:

{{
  "error_analysis": {{
    "category": "string (infrastructure, configuration, dependency, resource, security, network)",
    "severity": "string (critical, high, medium, low)",
    "root_cause": "string (detailed explanation of the underlying issue)",
    "affected_components": ["list of affected services/resources"],
    "error_pattern": "string (classification for learning purposes)"
  }},
  "immediate_actions": [
    {{
      "action": "string (specific action to take)",
      "command": "string (exact command or configuration change)",
      "reason": "string (why this action will help)",
      "risk_level": "string (low, medium, high)"
    }}
  ],
  "root_cause_fixes": [
    {{
      "fix": "string (permanent solution description)",
      "implementation": "string (how to implement this fix)",
      "prevention": "string (how to prevent this in future)",
      "testing": "string (how to verify the fix works)"
    }}
  ],
  "monitoring_recommendations": [
    {{
      "metric": "string (what to monitor)",
      "threshold": "string (alert threshold)",
      "action": "string (what to do when threshold is exceeded)"
    }}
  ],
  "confidence_score": "number (0.0-1.0, confidence in the diagnosis)",
  "estimated_resolution_time": "string (time estimate to fully resolve)",
  "requires_manual_intervention": "boolean (whether human intervention is needed)"
}}

Error Categories and Common Patterns:

**Infrastructure Errors**:
- Resource allocation failures (CPU, memory, storage)
- Network connectivity issues
- Platform-specific problems (Proxmox, K8s)
- Hardware failures

**Configuration Errors**:
- Invalid YAML/JSON syntax
- Missing required parameters
- Incorrect environment variables
- Service configuration mismatches

**Dependency Errors**:
- Missing dependencies
- Version incompatibilities
- Service startup order issues
- Database connection failures

**Resource Errors**:
- Insufficient permissions
- Storage space issues
- Memory/CPU limits exceeded
- Port conflicts

**Security Errors**:
- Authentication failures
- Certificate issues
- Firewall blocking
- Permission denied

**Network Errors**:
- DNS resolution failures
- Load balancer issues
- Service mesh problems
- SSL/TLS configuration

Analysis Guidelines:
1. Look for error patterns in logs
2. Check resource utilization and limits
3. Verify configuration syntax and values
4. Identify dependency chain issues
5. Consider timing and race conditions
6. Check for known issues with similar patterns
7. Evaluate security and permission settings

Provide specific, actionable solutions that can be automated where possible."""
)

ERROR_LEARNING_PROMPT = PromptTemplate(
    input_variables=["error_pattern", "successful_resolution", "failure_context"],
    template="""You are updating the error knowledge base with a new resolution pattern.

Error Pattern:
{error_pattern}

Successful Resolution:
{successful_resolution}

Failure Context:
{failure_context}

Create a knowledge base entry in JSON format:

{{
  "pattern_id": "string (unique identifier)",
  "pattern_name": "string (descriptive name)",
  "category": "string (error category)",
  "triggers": ["list of conditions that trigger this error"],
  "symptoms": ["list of observable symptoms"],
  "resolution_steps": [
    {{
      "step": "number",
      "action": "string",
      "command": "string (if applicable)",
      "expected_result": "string"
    }}
  ],
  "prevention_measures": ["list of preventive actions"],
  "automation_potential": "string (fully, partially, manual)",
  "confidence_level": "number (0.0-1.0)",
  "related_patterns": ["list of related pattern IDs"]
}}

This entry will be used to automatically diagnose and resolve similar issues in the future."""
)

HEALTH_CHECK_DIAGNOSIS_PROMPT = PromptTemplate(
    input_variables=["health_check_results", "service_metrics", "dependency_status"],
    template="""You are analyzing service health check failures.

Health Check Results:
{health_check_results}

Service Metrics:
{service_metrics}

Dependency Status:
{dependency_status}

Provide a health diagnosis in JSON format:

{{
  "overall_health": "string (healthy, degraded, unhealthy, critical)",
  "failing_checks": [
    {{
      "check_name": "string",
      "status": "string (failed, timeout, error)",
      "error_message": "string",
      "recommended_action": "string"
    }}
  ],
  "performance_issues": [
    {{
      "metric": "string",
      "current_value": "string",
      "threshold": "string", 
      "severity": "string",
      "impact": "string"
    }}
  ],
  "dependency_issues": [
    {{
      "service": "string",
      "status": "string",
      "impact_on_main_service": "string"
    }}
  ],
  "recovery_actions": [
    {{
      "priority": "number (1-5)",
      "action": "string",
      "automation_possible": "boolean"
    }}
  ]
}}"""
)