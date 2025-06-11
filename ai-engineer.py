#!/usr/bin/env python3

"""
AI Engineer - Entry Point

A sophisticated AI coding assistant with multi-provider support and advanced capabilities.
This tool provides intelligent code analysis, file operations, and programming guidance
through an interactive command-line interface.

Features:
- Multi-provider support (DeepSeek, OpenRouter)
- Advanced reasoning with chain-of-thought processing (with Reasoning models)
- Intelligent file operations (read, create, edit)
- Multi-file project understanding
- Interactive conversation with context retention
- Rich console interface with syntax highlighting   
- Dynamic model switching

Usage:
    python ai-engineer.py
    uv run ai-engineer.py

The assistant will start an interactive session where you can:
- Ask programming questions and get detailed explanations
- Request file operations that will be executed automatically
- Include files in the conversation using /add commands
- Switch between different AI models using /model commands
- Get help with debugging, optimization, and best practices

Environment Variables:
    DEEPSEEK_API_KEY - For DeepSeek models
    OPENROUTER_API_KEY - For OpenRouter models

Modular Structure:
- AI_engineer/config.py: Environment and multi-provider client setup
- AI_engineer/providers.py: Model and provider configurations
- AI_engineer/models.py: Pydantic models and data structures
- AI_engineer/tools.py: Function calling tools definitions
- AI_engineer/prompts.py: System prompts and templates
- AI_engineer/file_operations.py: File handling utilities
- AI_engineer/conversation.py: Conversation management
- AI_engineer/api_client.py: Multi-provider API integration
- AI_engineer/ui.py: Rich console and UI components
- AI_engineer/main.py: Main entry point and interactive loop
"""

from AI_engineer.main import main

if __name__ == "__main__":
    main()