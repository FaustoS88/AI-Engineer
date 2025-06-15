#!/usr/bin/env python3

import os
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style as PromptStyle
from .providers import (
    DEFAULT_MODEL, 
    get_model_config, 
    get_provider_config, 
    is_valid_model
)

# --------------------------------------------------------------------------------
# Environment and Configuration Setup
# --------------------------------------------------------------------------------

# Load environment variables from .env file
load_dotenv()

# Get configuration from environment variables
def get_configured_model() -> str:
    """Get the configured model from environment variables."""
    # Check if specific model is configured
    env_model = os.getenv("LLM_MODEL")
    if env_model and is_valid_model(env_model):
        return env_model
    
    # Check if provider is configured and use default model for that provider
    env_provider = os.getenv("LLM_PROVIDER", "").lower()
    if env_provider == "openrouter":
        return "anthropic/claude-sonnet-4"  # Default OpenRouter model
    elif env_provider == "deepseek":
        return "deepseek-reasoner"  # Default DeepSeek model
    
    # Fall back to global default
    return DEFAULT_MODEL

# Current model (can be changed at runtime)
current_model = get_configured_model()

# Initialize Rich console
console = Console()

# Initialize prompt session with custom styling
prompt_session = PromptSession(
    style=PromptStyle.from_dict({
        'prompt': '#0066ff bold',  # Bright blue prompt
        'completion-menu.completion': 'bg:#1e3a8a fg:#ffffff',
        'completion-menu.completion.current': 'bg:#3b82f6 fg:#ffffff bold',
    })
)


def get_client() -> Optional[OpenAI]:
    """Get the appropriate OpenAI client based on current model."""
    model_config = get_model_config(current_model)
    if not model_config:
        console.print(f"[red]Error: Unknown model '{current_model}'[/red]")
        return None
    
    provider_config = get_provider_config(model_config.provider)
    if not provider_config:
        console.print(f"[red]Error: Unknown provider '{model_config.provider}'[/red]")
        return None
    
    api_key = os.getenv(provider_config.api_key_env)
    if not api_key:
        console.print(f"[red]Error: {provider_config.api_key_env} environment variable not set[/red]")
        console.print(f"[yellow]Please set your API key for {provider_config.name}[/yellow]")
        return None
    
    # Create client with provider-specific configuration
    client_kwargs = {
        "api_key": api_key,
        "base_url": provider_config.base_url
    }
    
    try:
        return OpenAI(**client_kwargs)
    except Exception as e:
        console.print(f"[red]Error creating client: {e}[/red]")
        return None


def get_current_model() -> str:
    """Get the current model name."""
    return current_model


def set_current_model(model_name: str) -> bool:
    """Set the current model if it's valid."""
    global current_model
    if is_valid_model(model_name):
        current_model = model_name
        return True
    return False


def get_provider_headers() -> dict:
    """Get provider-specific headers for the current model."""
    model_config = get_model_config(current_model)
    if not model_config:
        return {}
    
    provider_config = get_provider_config(model_config.provider)
    if not provider_config or not provider_config.extra_headers:
        return {}
    
    return provider_config.extra_headers


def get_provider_extra_body() -> dict:
    """Get provider-specific extra body for the current model."""
    model_config = get_model_config(current_model)
    if not model_config:
        return {}
    
    provider_config = get_provider_config(model_config.provider)
    if not provider_config or not provider_config.extra_body:
        return {}
    
    return provider_config.extra_body


def supports_reasoning() -> bool:
    """Check if the current model supports reasoning content."""
    model_config = get_model_config(current_model)
    return model_config.supports_reasoning if model_config else False


def get_current_provider() -> str:
    """Get the current provider name."""
    model_config = get_model_config(current_model)
    return model_config.provider if model_config else "unknown"


# Display startup information
def display_startup_info():
    """Display startup configuration information."""
    model_config = get_model_config(current_model)
    if model_config:
        console.print(f"[dim]Configured model: {model_config.display_name} ({model_config.provider})[/dim]")
        
        # Check if API key is available
        provider_config = get_provider_config(model_config.provider)
        if provider_config:
            api_key = os.getenv(provider_config.api_key_env)
            if api_key:
                console.print(f"[dim green]✓ {provider_config.name} API key found[/dim green]")
            else:
                console.print(f"[dim red]✗ {provider_config.name} API key missing ({provider_config.api_key_env})[/dim red]")
    else:
        console.print(f"[dim red]✗ Unknown model: {current_model}[/dim red]")


# Legacy client for backward compatibility (will be deprecated)
client = get_client()

# --------------------------------------------------------------------------------
# Pydantic AI MCP Integration
# --------------------------------------------------------------------------------

from .pydantic_mcp_integration import get_manager, init_pydantic_mcp

def get_pydantic_mcp_manager():
    """Return the Pydantic MCP manager instance."""
    return get_manager()

def init_ai_system():
    """Initialize the AI system with Pydantic AI and MCP integration."""
    try:
        console.print("[dim]🤖 Initializing AI system...[/dim]")
        init_pydantic_mcp()
        console.print("[dim green]✅ AI system ready[/dim green]")
    except Exception as e:
        console.print(f"[dim red]⚠️ AI system initialization failed: {e}[/dim red]")