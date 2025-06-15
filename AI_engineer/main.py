#!/usr/bin/env python3

from .ui import (
    display_welcome, display_instructions, get_user_input,
    display_goodbye, display_session_finished, display_error,
    display_model_list, display_current_model, display_model_switched,
    display_invalid_model
)
from .file_operations import try_handle_add_command
from .api_client import stream_openai_response
from .config import set_current_model, display_startup_info, init_ai_system
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

def handle_mcp_command(user_input: str) -> bool:
    """Handle /mcp commands. Returns True if command was handled."""
    if not user_input.startswith("/mcp"):
        return False
    
    parts = user_input.split()
    if len(parts) < 2:
        subcommand = "list"
    else:
        subcommand = parts[1].lower()
    
    try:
        from .pydantic_mcp_integration import get_manager
        manager = get_manager()
        
        if subcommand == "list":
            from .ui import console
            console.print("[bold cyan]Pydantic AI MCP Servers:[/bold cyan]")
            
            # Read config directly to show current configuration state
            servers_info = _get_config_servers_info(manager)
            
            if not servers_info:
                console.print("[dim]No MCP servers configured[/dim]")
            else:
                enabled_count = len([s for s in servers_info if s['enabled']])
                total_count = len(servers_info)
                
                console.print(f"[green]📋 {total_count} server(s) configured, {enabled_count} enabled[/green]")
                
                for server_info in servers_info:
                    name = server_info['name']
                    command = server_info['command']
                    args = server_info.get('args', [])
                    enabled = server_info['enabled']
                    
                    # Build full command display
                    full_command = command
                    if args:
                        full_command += " " + " ".join(args)
                    
                    if enabled:
                        if manager._initialized and len(manager.mcp_servers) > 0:
                            status = "[green]✓ Active[/green]"
                        else:
                            status = "[yellow]○ Enabled (needs reload)[/yellow]"
                    else:
                        status = "[red]✗ Disabled[/red]"
                    
                    console.print(f"  • [bold]{name}[/bold] - {status}")
                    console.print(f"    Command: [dim]{full_command}[/dim]")
        
        elif subcommand == "reload":
            from .ui import console
            try:
                # Use the reload_config method
                manager.reload_config()
            except Exception as reload_error:
                console.print(f"[red]❌ Failed to reload MCP configuration: {reload_error}[/red]")
        
        elif subcommand in ["enable", "disable"]:
            if len(parts) < 3:
                from .ui import display_error
                display_error(f"Please specify a server name. Use '/mcp {subcommand} <server_name>'")
            else:
                server_name = parts[2]
                from .ui import console
                action = "Enabling" if subcommand == "enable" else "Disabling"
                console.print(f"[yellow]{action} MCP server: {server_name}[/yellow]")
                
                try:
                    success = _modify_server_status(manager, server_name, subcommand == "enable")
                    if success:
                        console.print(f"[green]✓ Server '{server_name}' {subcommand}d successfully[/green]")
                        console.print("[cyan]Use '/mcp reload' to apply changes[/cyan]")
                    else:
                        console.print(f"[red]❌ Server '{server_name}' not found in configuration[/red]")
                except Exception as e:
                    console.print(f"[red]❌ Failed to {subcommand} server: {e}[/red]")
        
        else:
            from .ui import display_error
            display_error("Available MCP commands:")
            display_error("  /mcp list              - List MCP servers")
            display_error("  /mcp reload            - Reload MCP configuration")
            display_error("  /mcp enable <server>   - Enable an MCP server")
            display_error("  /mcp disable <server>  - Disable an MCP server")
        
    except Exception as e:
        from .ui import display_error
        display_error(f"MCP command failed: {str(e)}")
    
    return True

def _get_config_servers_info(manager) -> list:
    """Get server information from config file."""
    import json
    
    servers_info = []
    try:
        if not manager.config_path.exists():
            return []
        
        with open(manager.config_path, 'r') as f:
            config = json.load(f)
        
        # Support Roo Code format (mcpServers)
        if "mcpServers" in config:
            for name, server_config in config["mcpServers"].items():
                servers_info.append({
                    'name': name,
                    'command': server_config.get("command", ""),
                    'args': server_config.get("args", []),
                    'enabled': not server_config.get("disabled", False)
                })
        
        # Support AI-Engineer format (servers)
        elif "servers" in config:
            for server_config in config["servers"]:
                servers_info.append({
                    'name': server_config.get("name", "Unknown"),
                    'command': server_config.get("command", ""),
                    'args': server_config.get("args", []),
                    'enabled': server_config.get("enabled", True)
                })
    
    except Exception as e:
        print(f"Error reading config: {e}")
    
    return servers_info

def _modify_server_status(manager, server_name: str, enable: bool) -> bool:
    """Modify server enabled/disabled status in the MCP config file."""
    import json
    
    try:
        if not manager.config_path.exists():
            return False
        
        # Read current config
        with open(manager.config_path, 'r') as f:
            config = json.load(f)
        
        # Modify server status
        modified = False
        
        # Handle Roo format (mcpServers)
        if "mcpServers" in config and server_name in config["mcpServers"]:
            config["mcpServers"][server_name]["disabled"] = not enable
            modified = True
        
        # Handle AI-Engineer format (servers)
        elif "servers" in config:
            for server_config in config["servers"]:
                if server_config.get("name") == server_name:
                    server_config["enabled"] = enable
                    modified = True
                    break
        
        if modified:
            # Write back to file
            with open(manager.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error modifying server status: {e}")
        return False

def main():
    """Main entry point for the AI Engineer application."""
    # Display startup information
    display_startup_info()
    
    # Initialize the AI system with Pydantic AI and MCP integration
    init_ai_system()
    
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

        # Handle /mcp commands
        if handle_mcp_command(user_input):
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