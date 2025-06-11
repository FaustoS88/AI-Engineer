#!/usr/bin/env python3

from .ui import (
    display_welcome, display_instructions, get_user_input,
    display_goodbye, display_session_finished, display_error,
    display_model_list, display_current_model, display_model_switched,
    display_invalid_model
)
from .file_operations import try_handle_add_command
from .api_client import stream_openai_response
from .config import set_current_model, display_startup_info
from .providers import is_valid_model

# --------------------------------------------------------------------------------
# Main Interactive Loop
# --------------------------------------------------------------------------------

def handle_model_command(user_input: str) -> bool:
    """Handle /model commands. Returns True if command was handled."""
    if not user_input.startswith("/model"):
        return False
    
    parts = user_input.split()
    if len(parts) < 2:
        display_error("Invalid model command. Use '/model list', '/model current', or '/model set <model_name>'")
        return True
    
    subcommand = parts[1].lower()
    
    if subcommand == "list":
        display_model_list()
    elif subcommand == "current":
        display_current_model()
    elif subcommand == "set":
        if len(parts) < 3:
            display_error("Please specify a model name. Use '/model set <model_name>'")
        else:
            model_name = parts[2]
            if is_valid_model(model_name):
                if set_current_model(model_name):
                    display_model_switched(model_name)
                else:
                    display_error(f"Failed to switch to model: {model_name}")
            else:
                display_invalid_model(model_name)
    else:
        display_error(f"Unknown model subcommand: {subcommand}")
        display_error("Available commands: list, current, set")
    
    return True

def main():
    """Main entry point for the AI Engineer application."""
    # Display startup information
    display_startup_info()
    
    # Display welcome and instructions
    display_welcome()
    display_instructions()

    # Main interactive loop
    while True:
        user_input = get_user_input()
        
        # Handle exit conditions
        if user_input is None:  # KeyboardInterrupt or EOFError
            break
            
        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            display_goodbye()
            break

        # Handle /model commands
        if handle_model_command(user_input):
            continue

        # Handle /add command
        if try_handle_add_command(user_input):
            continue

        # Process user message through API
        response_data = stream_openai_response(user_input)
        
        if response_data.get("error"):
            display_error(response_data['error'])

    display_session_finished()

if __name__ == "__main__":
    main()