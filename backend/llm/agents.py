"""LangChain agents for specialized tasks."""

from typing import Dict, List, Any, Optional
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.schema import BaseLanguageModel
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import json
import logging

from .prompts import (
    REQUIREMENT_ANALYSIS_PROMPT,
    IAC_GENERATION_PROMPT,
    ERROR_DIAGNOSIS_PROMPT
)

logger = logging.getLogger(__name__)


class RequirementAgent:
    """Agent specialized in analyzing and parsing user requirements."""

    def __init__(self, llm: BaseLanguageModel):
        self.llm = llm
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self._setup_tools()
        self._setup_agent()

    def _setup_tools(self) -> None:
        """Setup tools for the requirement agent."""
        self.tools = [
            Tool(
                name="validate_service_type",
                description="Validate if a service type is supported",
                func=self._validate_service_type
            ),
            Tool(
                name="estimate_resources",
                description="Estimate resource requirements for a service",
                func=self._estimate_resources
            ),
            Tool(
                name="suggest_dependencies",
                description="Suggest dependencies for a service type",
                func=self._suggest_dependencies
            ),
            Tool(
                name="check_compatibility",
                description="Check platform compatibility for requirements",
                func=self._check_compatibility
            )
        ]

    def _setup_agent(self) -> None:
        """Setup the LangChain agent."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert infrastructure architect specialized in analyzing deployment requirements.
            
            Your role is to:
            1. Parse natural language requirements into structured specifications
            2. Identify service types and dependencies
            3. Estimate resource requirements
            4. Suggest best practices and optimizations
            5. Validate configurations for feasibility
            
            Use the available tools to validate and enhance your analysis.
            Always provide structured JSON output following the deployment specification schema."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            max_iterations=5
        )

    async def analyze_requirements(
        self,
        user_request: str,
        available_templates: List[str],
        resource_constraints: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyze user requirements and generate specification."""
        try:
            # Prepare context for the agent
            analysis_context = {
                "user_request": user_request,
                "available_templates": available_templates,
                "resource_constraints": resource_constraints,
                "context": context or {}
            }

            # Use the agent to analyze requirements
            result = await self.agent_executor.ainvoke({
                "input": f"""
                Analyze the following deployment requirements:
                
                User Request: {user_request}
                Available Templates: {json.dumps(available_templates, indent=2)}
                Resource Constraints: {json.dumps(resource_constraints, indent=2)}
                Additional Context: {json.dumps(context or {}, indent=2)}
                
                Please provide a complete deployment specification in JSON format.
                """
            })

            # Parse the agent's response
            specification = self._parse_agent_response(result["output"])
            
            return {
                "success": True,
                "specification": specification,
                "confidence_score": self._calculate_confidence(specification, user_request),
                "analysis_steps": result.get("intermediate_steps", []),
                "warnings": self._validate_specification(specification),
                "assumptions": self._extract_assumptions(result["output"])
            }

        except Exception as e:
            logger.error(f"Requirements analysis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "specification": None
            }

    def _validate_service_type(self, service_type: str) -> str:
        """Validate if service type is supported."""
        supported_types = [
            "chat-service", "mcp-server", "database", "model-serving",
            "web-application", "api-service", "monitoring", "storage"
        ]
        
        if service_type.lower() in supported_types:
            return f"Service type '{service_type}' is supported"
        else:
            closest = min(supported_types, key=lambda x: abs(len(x) - len(service_type)))
            return f"Service type '{service_type}' not supported. Did you mean '{closest}'?"

    def _estimate_resources(self, service_description: str) -> str:
        """Estimate resource requirements based on service description."""
        # Simple heuristic-based estimation
        description_lower = service_description.lower()
        
        # Base requirements
        cpu_cores = 1.0
        memory_gb = 2.0
        storage_gb = 20.0
        gpu_required = False

        # Adjust based on keywords
        if any(word in description_lower for word in ["llm", "model", "ai", "ml"]):
            cpu_cores = max(cpu_cores, 4.0)
            memory_gb = max(memory_gb, 8.0)
            storage_gb = max(storage_gb, 100.0)
            gpu_required = True

        if any(word in description_lower for word in ["database", "db", "postgresql", "mysql"]):
            cpu_cores = max(cpu_cores, 2.0)
            memory_gb = max(memory_gb, 4.0)
            storage_gb = max(storage_gb, 50.0)

        if any(word in description_lower for word in ["high", "production", "scale"]):
            cpu_cores *= 2
            memory_gb *= 2
            storage_gb *= 1.5

        return json.dumps({
            "cpu_cores": cpu_cores,
            "memory_gb": memory_gb,
            "storage_gb": storage_gb,
            "gpu_required": gpu_required
        })

    def _suggest_dependencies(self, service_type: str) -> str:
        """Suggest common dependencies for a service type."""
        dependency_map = {
            "chat-service": [
                {"service": "database", "type": "postgresql", "required": True},
                {"service": "redis", "type": "cache", "required": False},
                {"service": "vector-db", "type": "embeddings", "required": False}
            ],
            "mcp-server": [
                {"service": "database", "type": "storage", "required": False}
            ],
            "model-serving": [
                {"service": "gpu-node", "type": "compute", "required": True},
                {"service": "model-storage", "type": "storage", "required": True}
            ],
            "web-application": [
                {"service": "database", "type": "postgresql", "required": True},
                {"service": "load-balancer", "type": "networking", "required": False}
            ]
        }

        dependencies = dependency_map.get(service_type, [])
        return json.dumps(dependencies)

    def _check_compatibility(self, requirements: str) -> str:
        """Check platform compatibility."""
        # Simple compatibility check
        req_dict = json.loads(requirements) if isinstance(requirements, str) else requirements
        
        issues = []
        warnings = []

        # Check resource limits
        if req_dict.get("cpu_cores", 0) > 32:
            issues.append("CPU requirement exceeds typical node capacity")
        
        if req_dict.get("memory_gb", 0) > 256:
            issues.append("Memory requirement exceeds typical node capacity")

        if req_dict.get("gpu_required") and req_dict.get("platform") == "basic":
            warnings.append("GPU required but basic platform selected")

        return json.dumps({
            "compatible": len(issues) == 0,
            "issues": issues,
            "warnings": warnings
        })

    def _parse_agent_response(self, response: str) -> Dict[str, Any]:
        """Parse the agent's response to extract JSON specification."""
        try:
            # Look for JSON in the response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback: create a basic specification
                return {
                    "service_type": "web-application",
                    "service_name": "unnamed-service",
                    "description": "Generated from requirements",
                    "template": "basic",
                    "resource_requirements": {
                        "cpu_cores": 1.0,
                        "memory_gb": 2.0,
                        "storage_gb": 20.0,
                        "gpu_required": False
                    }
                }
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON from agent response")
            return {}

    def _calculate_confidence(self, specification: Dict[str, Any], user_request: str) -> float:
        """Calculate confidence score for the analysis."""
        confidence = 0.5  # Base confidence
        
        # Increase confidence if specification is complete
        required_fields = ["service_type", "service_name", "description", "resource_requirements"]
        completed_fields = sum(1 for field in required_fields if field in specification)
        confidence += (completed_fields / len(required_fields)) * 0.3
        
        # Increase confidence if request was clear
        request_clarity_keywords = ["deploy", "create", "setup", "install", "configure"]
        if any(keyword in user_request.lower() for keyword in request_clarity_keywords):
            confidence += 0.2
        
        return min(confidence, 1.0)

    def _validate_specification(self, specification: Dict[str, Any]) -> List[str]:
        """Validate specification and return warnings."""
        warnings = []
        
        if not specification.get("service_name"):
            warnings.append("Service name not specified")
        
        if not specification.get("description"):
            warnings.append("Service description is missing")
        
        resources = specification.get("resource_requirements", {})
        if resources.get("cpu_cores", 0) < 0.5:
            warnings.append("CPU allocation might be too low")
        
        if resources.get("memory_gb", 0) < 1.0:
            warnings.append("Memory allocation might be too low")
        
        return warnings

    def _extract_assumptions(self, response: str) -> List[str]:
        """Extract assumptions made during analysis."""
        assumptions = []
        
        # Look for assumption indicators in the response
        assumption_indicators = ["assuming", "assume", "default", "typically", "usually"]
        
        for indicator in assumption_indicators:
            if indicator in response.lower():
                assumptions.append(f"Made assumptions based on '{indicator}' in analysis")
        
        return assumptions


class IaCAgent:
    """Agent specialized in generating Infrastructure as Code."""

    def __init__(self, llm: BaseLanguageModel):
        self.llm = llm
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self._setup_tools()
        self._setup_agent()

    def _setup_tools(self) -> None:
        """Setup tools for the IaC agent."""
        self.tools = [
            Tool(
                name="validate_terraform_syntax",
                description="Validate Terraform/OpenTofu syntax",
                func=self._validate_terraform_syntax
            ),
            Tool(
                name="check_resource_dependencies",
                description="Check resource dependencies",
                func=self._check_resource_dependencies
            ),
            Tool(
                name="optimize_configuration",
                description="Optimize infrastructure configuration",
                func=self._optimize_configuration
            )
        ]

    def _setup_agent(self) -> None:
        """Setup the LangChain agent."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert DevOps engineer specialized in Infrastructure as Code.
            
            Your role is to:
            1. Generate production-ready OpenTofu/Terraform configurations
            2. Follow security best practices
            3. Optimize for cost and performance
            4. Ensure proper resource dependencies
            5. Include monitoring and backup configurations
            
            Always generate complete, working configurations with proper documentation."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            max_iterations=5
        )

    async def generate_iac(
        self,
        deployment_spec: Dict[str, Any],
        template_base: str,
        target_platform: str = "proxmox",
        existing_resources: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate Infrastructure as Code configurations."""
        try:
            result = await self.agent_executor.ainvoke({
                "input": f"""
                Generate Infrastructure as Code for the following specification:
                
                Deployment Specification: {json.dumps(deployment_spec, indent=2)}
                Base Template: {template_base}
                Target Platform: {target_platform}
                Existing Resources: {json.dumps(existing_resources or {}, indent=2)}
                
                Please generate complete OpenTofu configuration files.
                """
            })

            files = self._parse_iac_files(result["output"])
            
            return {
                "success": True,
                "files": files,
                "generation_steps": result.get("intermediate_steps", []),
                "optimizations": self._extract_optimizations(result["output"])
            }

        except Exception as e:
            logger.error(f"IaC generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "files": {}
            }

    def _validate_terraform_syntax(self, config: str) -> str:
        """Basic Terraform syntax validation."""
        # Simple validation checks
        issues = []
        
        if "resource" not in config:
            issues.append("No resources defined")
        
        if config.count("{") != config.count("}"):
            issues.append("Mismatched braces")
        
        if config.count('"') % 2 != 0:
            issues.append("Mismatched quotes")
        
        return json.dumps({
            "valid": len(issues) == 0,
            "issues": issues
        })

    def _check_resource_dependencies(self, resources: str) -> str:
        """Check resource dependencies."""
        # Simple dependency analysis
        dependencies = []
        
        if "database" in resources.lower():
            dependencies.append("Network configuration required")
        
        if "vm" in resources.lower():
            dependencies.append("Storage pool required")
        
        return json.dumps({"dependencies": dependencies})

    def _optimize_configuration(self, config: str) -> str:
        """Suggest configuration optimizations."""
        optimizations = []
        
        if "cpu" in config.lower():
            optimizations.append("Consider CPU affinity for performance")
        
        if "memory" in config.lower():
            optimizations.append("Enable memory ballooning for efficiency")
        
        return json.dumps({"optimizations": optimizations})

    def _parse_iac_files(self, response: str) -> Dict[str, str]:
        """Parse IaC files from agent response."""
        files = {}
        
        # Look for code blocks in the response
        import re
        code_blocks = re.findall(r'```(?:hcl|terraform)?\n(.*?)\n```', response, re.DOTALL)
        
        for i, block in enumerate(code_blocks):
            filename = f"main_{i}.tf" if i == 0 else f"additional_{i}.tf"
            files[filename] = block.strip()
        
        return files

    def _extract_optimizations(self, response: str) -> List[str]:
        """Extract optimization suggestions from response."""
        optimizations = []
        
        if "optimize" in response.lower():
            optimizations.append("Configuration includes optimization suggestions")
        
        return optimizations


class ErrorAnalysisAgent:
    """Agent specialized in error diagnosis and resolution."""

    def __init__(self, llm: BaseLanguageModel):
        self.llm = llm
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self._setup_tools()
        self._setup_agent()

    def _setup_tools(self) -> None:
        """Setup tools for the error analysis agent."""
        self.tools = [
            Tool(
                name="categorize_error",
                description="Categorize the type of error",
                func=self._categorize_error
            ),
            Tool(
                name="suggest_fixes",
                description="Suggest potential fixes for errors",
                func=self._suggest_fixes
            ),
            Tool(
                name="check_known_issues",
                description="Check against known issue database",
                func=self._check_known_issues
            )
        ]

    def _setup_agent(self) -> None:
        """Setup the LangChain agent."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert DevOps troubleshooter specialized in infrastructure deployments.
            
            Your role is to:
            1. Analyze error logs and system states
            2. Identify root causes of failures
            3. Provide actionable resolution steps
            4. Suggest preventive measures
            5. Categorize errors for learning purposes
            
            Always provide structured, actionable solutions with clear priorities."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            max_iterations=5
        )

    async def diagnose_error(
        self,
        error_logs: str,
        deployment_config: Dict[str, Any],
        system_state: Dict[str, Any],
        previous_fixes: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Diagnose deployment errors."""
        try:
            result = await self.agent_executor.ainvoke({
                "input": f"""
                Analyze the following deployment error:
                
                Error Logs: {error_logs}
                Deployment Config: {json.dumps(deployment_config, indent=2)}
                System State: {json.dumps(system_state, indent=2)}
                Previous Fixes Attempted: {json.dumps(previous_fixes or [], indent=2)}
                
                Please provide a complete error diagnosis with immediate actions and root cause fixes.
                """
            })

            diagnosis = self._parse_diagnosis(result["output"])
            
            return {
                "success": True,
                "diagnosis": diagnosis,
                "analysis_steps": result.get("intermediate_steps", [])
            }

        except Exception as e:
            logger.error(f"Error diagnosis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "diagnosis": None
            }

    def _categorize_error(self, error_log: str) -> str:
        """Categorize the error type."""
        error_lower = error_log.lower()
        
        if any(word in error_lower for word in ["connection", "network", "dns"]):
            category = "network"
        elif any(word in error_lower for word in ["permission", "access", "denied"]):
            category = "security"
        elif any(word in error_lower for word in ["memory", "cpu", "disk"]):
            category = "resource"
        elif any(word in error_lower for word in ["config", "parameter", "setting"]):
            category = "configuration"
        else:
            category = "unknown"
        
        return json.dumps({"category": category})

    def _suggest_fixes(self, error_description: str) -> str:
        """Suggest potential fixes."""
        fixes = []
        error_lower = error_description.lower()
        
        if "connection" in error_lower:
            fixes.append("Check network connectivity and firewall rules")
        
        if "permission" in error_lower:
            fixes.append("Verify user permissions and access rights")
        
        if "memory" in error_lower:
            fixes.append("Increase memory allocation or check for memory leaks")
        
        return json.dumps({"suggested_fixes": fixes})

    def _check_known_issues(self, error_pattern: str) -> str:
        """Check against known issues."""
        # This would query a database of known issues
        # For now, return a placeholder
        return json.dumps({
            "known_issue": False,
            "similar_issues": [],
            "documented_solutions": []
        })

    def _parse_diagnosis(self, response: str) -> Dict[str, Any]:
        """Parse diagnosis from agent response."""
        # Try to extract structured data from response
        try:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # Fallback: create basic diagnosis structure
        return {
            "error_analysis": {
                "category": "unknown",
                "severity": "medium",
                "root_cause": "Analysis in progress",
                "affected_components": [],
                "error_pattern": "unclassified"
            },
            "immediate_actions": [],
            "root_cause_fixes": [],
            "monitoring_recommendations": [],
            "confidence_score": 0.5,
            "estimated_resolution_time": "unknown",
            "requires_manual_intervention": True
        }