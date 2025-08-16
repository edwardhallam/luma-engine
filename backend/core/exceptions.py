"""Custom exceptions for AI Infrastructure Deployer."""

from typing import Optional, Dict, Any


class AIDException(Exception):
    """Base exception for AI Infrastructure Deployer."""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationException(AIDException):
    """Exception raised for validation errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=400, details=details)


class ResourceNotFoundException(AIDException):
    """Exception raised when a resource is not found."""
    
    def __init__(self, resource_type: str, resource_id: str):
        message = f"{resource_type} with ID '{resource_id}' not found"
        super().__init__(message, status_code=404)


class InfrastructureException(AIDException):
    """Exception raised for infrastructure-related errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=503, details=details)


class LLMException(AIDException):
    """Exception raised for LLM service errors."""
    
    def __init__(self, message: str, provider: Optional[str] = None):
        details = {"provider": provider} if provider else {}
        super().__init__(message, status_code=502, details=details)


class DeploymentException(AIDException):
    """Exception raised for deployment-related errors."""
    
    def __init__(self, message: str, deployment_id: Optional[str] = None):
        details = {"deployment_id": deployment_id} if deployment_id else {}
        super().__init__(message, status_code=500, details=details)


class TemplateException(AIDException):
    """Exception raised for template-related errors."""
    
    def __init__(self, message: str, template_id: Optional[str] = None):
        details = {"template_id": template_id} if template_id else {}
        super().__init__(message, status_code=400, details=details)


class AuthenticationException(AIDException):
    """Exception raised for authentication errors."""
    
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message, status_code=401)


class AuthorizationException(AIDException):
    """Exception raised for authorization errors."""
    
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, status_code=403)


class ConfigurationException(AIDException):
    """Exception raised for configuration errors."""
    
    def __init__(self, message: str, config_key: Optional[str] = None):
        details = {"config_key": config_key} if config_key else {}
        super().__init__(message, status_code=500, details=details)


class ExternalServiceException(AIDException):
    """Exception raised for external service errors."""
    
    def __init__(self, service_name: str, message: str):
        details = {"service": service_name}
        super().__init__(f"{service_name}: {message}", status_code=502, details=details)


class WorkflowException(AIDException):
    """Exception raised for workflow execution errors."""
    
    def __init__(self, message: str, workflow_id: Optional[str] = None):
        details = {"workflow_id": workflow_id} if workflow_id else {}
        super().__init__(message, status_code=500, details=details)