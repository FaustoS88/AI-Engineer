"""
AI Engineer - An AI-powered coding assistant with multi-provider support and function calling capabilities.

This package provides a modular, interactive coding assistant that can:
- Read and analyze code files
- Create and edit files with precision
- Provide expert-level programming guidance
- Handle complex multi-file operations
- Support multiple LLM providers (DeepSeek, OpenRouter)

The assistant uses advanced reasoning capabilities combined with function calling
to provide thoughtful, well-structured solutions while explaining the reasoning process.

Main modules:
- main: Entry point and interactive loop
- config: Environment setup and configuration
- providers: Multi-provider model configurations
- api_client: OpenAI API integration with streaming
- tools: Function calling tool definitions
- prompts: System prompts and templates
- file_operations: File handling and manipulation
- conversation: Conversation history management
- models: Pydantic data models
- ui: Rich console interface components

Usage:
    from deepseek_engineer.main import main
    main()
"""

__version__ = "2.0.0"
__author__ = "AI Engineer Team"
__description__ = "AI-powered coding assistant with multi-provider support"

# Import main components for easy access
from .main import main
from .config import console, prompt_session, get_current_model, set_current_model
from .models import FileToCreate, FileToEdit
from .providers import get_all_models, get_model_config, is_valid_model

__all__ = [
    "main",
    "console",
    "prompt_session",
    "get_current_model",
    "set_current_model",
    "get_all_models",
    "get_model_config",
    "is_valid_model",
    "FileToCreate",
    "FileToEdit"
]