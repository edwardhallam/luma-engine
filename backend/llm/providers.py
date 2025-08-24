"""LLM provider implementations."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from langchain.schema import BaseLanguageModel
from langchain_anthropic import ChatAnthropic
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._client: Optional[BaseLanguageModel] = None

    @abstractmethod
    def get_client(self) -> BaseLanguageModel:
        """Get the LLM client instance."""
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """Validate provider configuration."""
        pass

    @property
    def name(self) -> str:
        """Get provider name."""
        return self.__class__.__name__.replace("Provider", "").lower()


class OpenAIProvider(LLMProvider):
    """OpenAI provider implementation."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.model = config.get("model", "gpt-4")
        self.temperature = config.get("temperature", 0.1)
        self.max_tokens = config.get("max_tokens", 4000)

    def validate_config(self) -> bool:
        """Validate OpenAI configuration."""
        if not self.api_key:
            logger.error("OpenAI API key is required")
            return False
        return True

    def get_client(self) -> BaseLanguageModel:
        """Get OpenAI client."""
        if not self._client:
            if not self.validate_config():
                raise ValueError("Invalid OpenAI configuration")

            self._client = ChatOpenAI(
                api_key=self.api_key,
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
        return self._client


class AnthropicProvider(LLMProvider):
    """Anthropic provider implementation."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.model = config.get("model", "claude-3-sonnet-20240229")
        self.temperature = config.get("temperature", 0.1)
        self.max_tokens = config.get("max_tokens", 4000)

    def validate_config(self) -> bool:
        """Validate Anthropic configuration."""
        if not self.api_key:
            logger.error("Anthropic API key is required")
            return False
        return True

    def get_client(self) -> BaseLanguageModel:
        """Get Anthropic client."""
        if not self._client:
            if not self.validate_config():
                raise ValueError("Invalid Anthropic configuration")

            self._client = ChatAnthropic(
                api_key=self.api_key,
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
        return self._client


class OllamaProvider(LLMProvider):
    """Ollama provider implementation for local models."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get("base_url", "http://localhost:11434")
        self.model = config.get("model", "llama2")
        self.temperature = config.get("temperature", 0.1)

    def validate_config(self) -> bool:
        """Validate Ollama configuration."""
        try:
            import requests

            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            available_models = [
                model["name"] for model in response.json().get("models", [])
            ]
            if self.model not in available_models:
                logger.warning(
                    f"Model {self.model} not found in Ollama. Available: {available_models}"
                )
                return False
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            return False

    def get_client(self) -> BaseLanguageModel:
        """Get Ollama client."""
        if not self._client:
            if not self.validate_config():
                raise ValueError("Invalid Ollama configuration")

            self._client = Ollama(
                base_url=self.base_url,
                model=self.model,
                temperature=self.temperature,
            )
        return self._client


class ProviderFactory:
    """Factory for creating LLM providers."""

    _providers = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "ollama": OllamaProvider,
    }

    @classmethod
    def create_provider(cls, provider_type: str, config: Dict[str, Any]) -> LLMProvider:
        """Create a provider instance."""
        if provider_type not in cls._providers:
            raise ValueError(f"Unknown provider type: {provider_type}")

        provider_class = cls._providers[provider_type]
        return provider_class(config)

    @classmethod
    def get_available_providers(cls) -> List[str]:
        """Get list of available provider types."""
        return list(cls._providers.keys())

    @classmethod
    def register_provider(cls, name: str, provider_class: type) -> None:
        """Register a custom provider."""
        cls._providers[name] = provider_class
