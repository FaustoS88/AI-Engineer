#!/usr/bin/env python3

from rich.panel import Panel
from rich.table import Table
from .config import console, prompt_session, get_current_model
from .providers import get_model_config, get_all_models, get_models_by_provider

# --------------------------------------------------------------------------------
# UI Components and Interface
# --------------------------------------------------------------------------------

def display_welcome():
    """Display the welcome panel."""
    current_model = get_current_model()
    model_config = get_model_config(current_model)
    
    # Create a beautiful gradient-style welcome panel
    welcome_text = f"""[bold bright_green]🤖 AI Engineer[/bold bright_green] [bright_cyan]with Multi-Provider Support[/bright_cyan]
[dim green]Current Model: {model_config.display_name if model_config else current_model}[/dim green]
[dim green]Provider: {model_config.provider.title() if model_config else 'Unknown'}[/dim green]"""
    
    console.print(Panel.fit(
        welcome_text,
        border_style="bright_green",
        padding=(1, 2),
        title="[bold bright_green]🤖 AI Code Assistant[/bold bright_green]",
        title_align="center"
    ))

def display_instructions():
    """Display the instruction panel."""
    # Create an elegant instruction panel
    instructions = """[bold bright_green]📁 File Operations:[/bold bright_green]
  • [bright_cyan]/add path/to/file[/bright_cyan] - Include a single file in conversation
  • [bright_cyan]/add path/to/folder[/bright_cyan] - Include all files in a folder
  • [dim]The AI can automatically read and create files using function calls[/dim]

[bold bright_green]🔧 Model Management:[/bold bright_green]
  • [bright_cyan]/model list[/bright_cyan] - Show all available models
  • [bright_cyan]/model set <model_name>[/bright_cyan] - Switch to a specific model
  • [bright_cyan]/model current[/bright_cyan] - Show currently selected model

[bold bright_green]🔌 MCP (Model Context Protocol):[/bold bright_green]
  • [bright_cyan]/mcp list[/bright_cyan] - Show all MCP servers and their tools
  • [bright_cyan]/mcp enable <server>[/bright_cyan] - Enable an MCP server
  • [bright_cyan]/mcp disable <server>[/bright_cyan] - Disable an MCP server
  • [bright_cyan]/mcp reload[/bright_cyan] - Reload MCP configuration

[bold bright_green]🎯 Commands:[/bold bright_green]
  • [bright_cyan]exit[/bright_cyan] or [bright_cyan]quit[/bright_cyan] - End the session
  • Just ask naturally - the AI will handle file operations automatically!"""
    
    console.print(Panel(
        instructions,
        border_style="green",
        padding=(1, 2),
        title="[bold green]💡 How to Use[/bold green]",
        title_align="left"
    ))
    console.print()

def get_user_input() -> str:
    """Get user input with styled prompt."""
    try:
        current_model = get_current_model()
        model_config = get_model_config(current_model)
        provider_name = model_config.provider.title() if model_config else "Unknown"
        return prompt_session.prompt(f"🟢 You ({provider_name})> ").strip()
    except (EOFError, KeyboardInterrupt):
        console.print("\n[bold yellow]👋 Exiting gracefully...[/bold yellow]")
        return None

def display_goodbye():
    """Display goodbye message."""
    console.print("[bold bright_green]👋 Goodbye! Happy coding![/bold bright_green]")

def display_session_finished():
    """Display session finished message."""
    console.print("[bold green]✨ Session finished. Thank you for using AI Engineer![/bold green]")

def display_error(error_message: str):
    """Display error message."""
    console.print(f"[bold red]❌ Error: {error_message}[/bold red]")

def display_model_list():
    """Display all available models in a formatted table."""
    models = get_all_models()
    current_model = get_current_model()
    
    # Group models by provider
    providers = {}
    for model in models:
        if model.provider not in providers:
            providers[model.provider] = []
        providers[model.provider].append(model)
    
    console.print("\n[bold bright_blue]📋 Available Models:[/bold bright_blue]")
    
    for provider_name, provider_models in providers.items():
        table = Table(title=f"{provider_name.title()} Models", show_header=True, header_style="bold magenta")
        table.add_column("Model Name", style="cyan", no_wrap=True)
        table.add_column("Display Name", style="white")
        table.add_column("Features", style="dim")
        table.add_column("Status", style="green")
        
        for model in provider_models:
            features = []
            if model.supports_reasoning:
                features.append("Reasoning")
            features_str = ", ".join(features) if features else "Standard"
            
            status = "🟢 Current" if model.name == current_model else "⚪ Available"
            
            table.add_row(
                model.name,
                model.display_name,
                features_str,
                status
            )
        
        console.print(table)
        console.print()

def display_current_model():
    """Display the currently selected model."""
    current_model = get_current_model()
    model_config = get_model_config(current_model)
    
    if model_config:
        console.print(f"\n[bold bright_blue]Current Model:[/bold bright_blue] {model_config.display_name}")
        console.print(f"[bold bright_blue]Provider:[/bold bright_blue] {model_config.provider.title()}")
        console.print(f"[bold bright_blue]Model ID:[/bold bright_blue] {model_config.name}")
        if model_config.supports_reasoning:
            console.print("[bold bright_blue]Features:[/bold bright_blue] Chain-of-Thought Reasoning")
        console.print()
    else:
        console.print(f"\n[bold red]Unknown model: {current_model}[/bold red]")

def display_model_switched(model_name: str):
    """Display confirmation that model was switched."""
    model_config = get_model_config(model_name)
    if model_config:
        console.print(f"\n[bold green]✅ Switched to {model_config.display_name} ({model_config.provider.title()})[/bold green]")
    else:
        console.print(f"\n[bold green]✅ Switched to {model_name}[/bold green]")

def display_invalid_model(model_name: str):
    """Display error for invalid model."""
    console.print(f"\n[bold red]❌ Invalid model: {model_name}[/bold red]")
    console.print("[dim]Use '/model list' to see available models[/dim]")