"""Main LLM service orchestrating all LLM operations."""

import json
import logging
from typing import Any, Dict, List, Optional

from langchain.chains import LLMChain
from langchain_core.language_models import BaseLanguageModel

from .prompts import (
    ERROR_DIAGNOSIS_PROMPT,
    IAC_GENERATION_PROMPT,
    REQUIREMENT_ANALYSIS_PROMPT,
)
from .providers import LLMProvider, ProviderFactory

logger = logging.getLogger(__name__)


class LLMService:
    """Main service for LLM operations."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.providers: Dict[str, LLMProvider] = {}
        self.primary_provider: Optional[str] = None
        self.fallback_providers: List[str] = []
        self._initialize_providers()

    def _initialize_providers(self) -> None:
        """Initialize configured LLM providers."""
        provider_configs = self.config.get("providers", {})

        for provider_name, provider_config in provider_configs.items():
            if provider_config.get("enabled", False):
                try:
                    provider = ProviderFactory.create_provider(
                        provider_name, provider_config
                    )
                    if provider.validate_config():
                        self.providers[provider_name] = provider
                        logger.info(f"Initialized {provider_name} provider")

                        # Set primary and fallback providers
                        if provider_config.get("primary", False):
                            self.primary_provider = provider_name
                        if provider_config.get("fallback", False):
                            self.fallback_providers.append(provider_name)
                    else:
                        logger.warning(
                            f"Invalid configuration for {provider_name} provider"
                        )
                except Exception as e:
                    logger.error(f"Failed to initialize {provider_name} provider: {e}")

        if not self.primary_provider and self.providers:
            self.primary_provider = list(self.providers.keys())[0]
            logger.info(f"Set {self.primary_provider} as default primary provider")

    def get_llm(self, provider_name: Optional[str] = None) -> BaseLanguageModel:
        """Get LLM client for specified provider or primary."""
        if provider_name and provider_name in self.providers:
            return self.providers[provider_name].get_client()
        elif self.primary_provider:
            return self.providers[self.primary_provider].get_client()
        else:
            raise ValueError("No LLM providers available")

    async def analyze_requirements(
        self,
        user_request: str,
        available_templates: List[str],
        resource_constraints: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Analyze user requirements and generate deployment specification."""
        try:
            llm = self.get_llm()
            chain = LLMChain(llm=llm, prompt=REQUIREMENT_ANALYSIS_PROMPT)

            response = await chain.arun(
                user_request=user_request,
                available_templates=json.dumps(available_templates, indent=2),
                resource_constraints=json.dumps(resource_constraints, indent=2),
            )

            # Parse JSON response
            try:
                spec = json.loads(response.strip())
                return {
                    "success": True,
                    "specification": spec,
                    "provider_used": self.primary_provider,
                }
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse LLM response as JSON: {e}")
                return {
                    "success": False,
                    "error": "Invalid JSON response from LLM",
                    "raw_response": response,
                }

        except Exception as e:
            logger.error(f"Requirements analysis failed: {e}")
            return await self._try_fallback_providers(
                "analyze_requirements",
                {
                    "user_request": user_request,
                    "available_templates": available_templates,
                    "resource_constraints": resource_constraints,
                },
            )

    async def generate_iac(
        self,
        deployment_spec: Dict[str, Any],
        template_base: str,
        target_platform: str = "proxmox",
        existing_resources: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate Infrastructure as Code configurations."""
        try:
            llm = self.get_llm()
            chain = LLMChain(llm=llm, prompt=IAC_GENERATION_PROMPT)

            response = await chain.arun(
                deployment_spec=json.dumps(deployment_spec, indent=2),
                template_base=template_base,
                target_platform=target_platform,
                existing_resources=json.dumps(existing_resources or {}, indent=2),
            )

            # Parse the response to extract files
            files = self._parse_iac_response(response)

            return {
                "success": True,
                "files": files,
                "raw_response": response,
                "provider_used": self.primary_provider,
            }

        except Exception as e:
            logger.error(f"IaC generation failed: {e}")
            return await self._try_fallback_providers(
                "generate_iac",
                {
                    "deployment_spec": deployment_spec,
                    "template_base": template_base,
                    "target_platform": target_platform,
                    "existing_resources": existing_resources,
                },
            )

    async def diagnose_error(
        self,
        error_logs: str,
        deployment_config: Dict[str, Any],
        system_state: Dict[str, Any],
        previous_fixes: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Diagnose deployment errors and provide solutions."""
        try:
            llm = self.get_llm()
            chain = LLMChain(llm=llm, prompt=ERROR_DIAGNOSIS_PROMPT)

            response = await chain.arun(
                error_logs=error_logs,
                deployment_config=json.dumps(deployment_config, indent=2),
                system_state=json.dumps(system_state, indent=2),
                previous_fixes=json.dumps(previous_fixes or [], indent=2),
            )

            # Parse JSON response
            try:
                diagnosis = json.loads(response.strip())
                return {
                    "success": True,
                    "diagnosis": diagnosis,
                    "provider_used": self.primary_provider,
                }
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse error diagnosis response: {e}")
                return {
                    "success": False,
                    "error": "Invalid JSON response from LLM",
                    "raw_response": response,
                }

        except Exception as e:
            logger.error(f"Error diagnosis failed: {e}")
            return await self._try_fallback_providers(
                "diagnose_error",
                {
                    "error_logs": error_logs,
                    "deployment_config": deployment_config,
                    "system_state": system_state,
                    "previous_fixes": previous_fixes,
                },
            )

    def _parse_iac_response(self, response: str) -> Dict[str, str]:
        """Parse IaC response to extract individual files."""
        files = {}
        lines = response.split("\n")
        current_file = None
        current_content = []

        for line in lines:
            if line.startswith("# filename:"):
                # Save previous file
                if current_file and current_content:
                    files[current_file] = "\n".join(current_content)

                # Start new file
                current_file = line.replace("# filename:", "").strip()
                current_content = []
            elif line.startswith("```hcl") or line.startswith("```"):
                continue
            elif current_file:
                current_content.append(line)

        # Save last file
        if current_file and current_content:
            files[current_file] = "\n".join(current_content)

        return files

    async def _try_fallback_providers(
        self, method_name: str, kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Try fallback providers if primary fails."""
        for provider_name in self.fallback_providers:
            try:
                logger.info(f"Trying fallback provider: {provider_name}")

                # Temporarily switch to fallback provider
                original_primary = self.primary_provider
                self.primary_provider = provider_name

                # Retry the method
                if method_name == "analyze_requirements":
                    result = await self.analyze_requirements(**kwargs)
                elif method_name == "generate_iac":
                    result = await self.generate_iac(**kwargs)
                elif method_name == "diagnose_error":
                    result = await self.diagnose_error(**kwargs)
                else:
                    raise ValueError(f"Unknown method: {method_name}")

                # Restore original primary
                self.primary_provider = original_primary

                if result.get("success"):
                    result["provider_used"] = provider_name
                    return result

            except Exception as e:
                logger.error(f"Fallback provider {provider_name} also failed: {e}")
                continue

        return {
            "success": False,
            "error": "All providers failed",
            "providers_tried": [self.primary_provider] + self.fallback_providers,
        }

    def get_provider_status(self) -> Dict[str, Any]:
        """Get status of all configured providers."""
        status = {}
        for name, provider in self.providers.items():
            try:
                # Test provider availability by getting client
                provider.get_client()  # Just test connectivity
                status[name] = {
                    "available": True,
                    "primary": name == self.primary_provider,
                    "fallback": name in self.fallback_providers,
                    "config": {
                        k: v for k, v in provider.config.items() if k != "api_key"
                    },
                }
            except Exception as e:
                status[name] = {
                    "available": False,
                    "error": str(e),
                    "primary": name == self.primary_provider,
                    "fallback": name in self.fallback_providers,
                }

        return status
