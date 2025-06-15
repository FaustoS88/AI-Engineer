"""
Provider configurations for different LLM providers.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ModelConfig:
    """Configuration for a specific model."""
    name: str
    provider: str
    display_name: str
    supports_reasoning: bool = False
    max_tokens: Optional[int] = None


@dataclass
class ProviderConfig:
    """Configuration for a provider."""
    name: str
    base_url: str
    api_key_env: str
    extra_headers: Optional[Dict[str, str]] = None
    extra_body: Optional[Dict] = None


# Provider configurations
PROVIDERS = {
    "deepseek": ProviderConfig(
        name="DeepSeek",
        base_url="https://api.deepseek.com",
        api_key_env="DEEPSEEK_API_KEY"
    ),
    "openrouter": ProviderConfig(
        name="OpenRouter",
        base_url="https://openrouter.ai/api/v1",
        api_key_env="OPENROUTER_API_KEY",
        extra_body={}
    ),
    "mcp": ProviderConfig(
        name="MCP Local",
        base_url="http://localhost",  # Not used, but keeps interface happy
        api_key_env=""  # No API key needed for MCP
    )
}

# Available models
MODELS = {
    # DeepSeek models
    "deepseek-reasoner": ModelConfig(
        name="deepseek-reasoner",
        provider="deepseek",
        display_name="DeepSeek Reasoner",
        supports_reasoning=True
    ),
    "deepseek-chat": ModelConfig(
        name="deepseek-chat",
        provider="deepseek",
        display_name="DeepSeek Chat",
        supports_reasoning=False
    ),
    
    # OpenRouter models
    "anthropic/claude-sonnet-4": ModelConfig(
        name="anthropic/claude-sonnet-4",
        provider="openrouter",
        display_name="Anthropic Claude Sonnet 4"
    ),
    "anthropic/claude-3.7-sonnet:thinking": ModelConfig(
        name="anthropic/claude-3.7-sonnet:thinking",
        provider="openrouter",
        display_name="anthropic Claude-3.7-sonnet-thinking",
        supports_reasoning=True
    ),
    "anthropic/claude-3.7-sonnet": ModelConfig(
        name="anthropic/claude-3.7-sonnet",
        provider="openrouter",
        display_name="anthropic Claude-3.7-sonnet"
    ),
    "openai/o3-mini-high": ModelConfig(
        name="openai/o3-mini-high",
        provider="openrouter",
        display_name="OpenAI GPT-o3-mini-high",
        supports_reasoning=True
    ),
    "openai/gpt-4.1": ModelConfig(
        name="openai/gpt-4.1",
        provider="openrouter",
        display_name="OpenAI GPT-4.1"
    ),
    "google/gemini-2.5-pro-preview": ModelConfig(
        name="google/gemini-2.5-pro-preview",
        provider="openrouter",
        display_name="Google: Gemini 2.5 Pro Preview 06-05",
        supports_reasoning=True
    ),
    "google/gemini-2.5-flash-preview-05-20": ModelConfig(
        name="google/gemini-2.5-flash-preview-05-20",
        provider="openrouter",
        display_name="Google: Gemini 2.5 Flash Preview 05-20"
    )
}

# Default model
DEFAULT_MODEL = "deepseek-reasoner"


def get_model_config(model_name: str) -> Optional[ModelConfig]:
    """Get configuration for a specific model."""
    return MODELS.get(model_name)


def get_provider_config(provider_name: str) -> Optional[ProviderConfig]:
    """Get configuration for a specific provider."""
    return PROVIDERS.get(provider_name)


def get_models_by_provider(provider_name: str) -> List[ModelConfig]:
    """Get all models for a specific provider."""
    return [model for model in MODELS.values() if model.provider == provider_name]


def get_all_models() -> List[ModelConfig]:
    """Get all available models."""
    return list(MODELS.values())


def is_valid_model(model_name: str) -> bool:
    """Check if a model name is valid."""
    return model_name in MODELS