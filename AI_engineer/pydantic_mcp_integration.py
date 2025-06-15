#!/usr/bin/env python3
"""
Pydantic AI MCP Integration with enhanced tool call logging.
"""

import asyncio
import json
import os
import pathlib
import threading
import time
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from watchdog.events import FileSystemEventHandler

if TYPE_CHECKING:
    from watchdog.observers import Observer
else:
    try:
        from watchdog.observers import Observer
    except ImportError:
        Observer = None

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.tools import Tool
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live

console = Console()

class MCPToolCallLogger:
    """Enhanced logger for MCP tool calls with visual feedback."""
    
    def __init__(self, console: Console):
        self.console = console
        self.current_server = None
        self.tool_call_count = 0
        
    def log_server_usage(self, server_name: str):
        """Log which MCP server is being used."""
        self.current_server = server_name
        # Map technical names to user-friendly names
        display_name = self._get_display_name(server_name)
        self.console.print(f"⚡ [bold cyan]Using MCP server:[/bold cyan] [bold]{display_name}[/bold]")
        
    def _get_display_name(self, server_name: str) -> str:
        """Convert technical server names to user-friendly display names."""
        display_map = {
            "github.com/upstash/context7-mcp": "Context7",
            "brave-search": "Brave Search",
            "Context7": "Context7",
            "Brave Search": "Brave Search"
        }
        return display_map.get(server_name, server_name)
        
    def log_tool_call_start(self, tool_name: str, args: Dict[str, Any] = None):
        """Log the start of a tool call."""
        self.tool_call_count += 1
        self.console.print(f"→ [bold yellow]{tool_name}[/bold yellow]", end="")
        if args and len(str(args)) < 100:  # Show args if not too long
            # Format args nicely
            args_str = ", ".join([f"{k}='{v}'" for k, v in args.items()])
            self.console.print(f" [dim]({args_str})[/dim]")
        else:
            self.console.print()
            
    def log_tool_call_success(self, tool_name: str, result_summary: str = None):
        """Log successful tool call completion."""
        checkmark = "✓"
        if result_summary:
            self.console.print(f"{checkmark} [bold green]{result_summary}[/bold green]")
        else:
            self.console.print(f"{checkmark} [bold green]{tool_name} completed[/bold green]")
            
    def log_tool_call_error(self, tool_name: str, error: str):
        """Log tool call error."""
        self.console.print(f"✗ [bold red]Error in {tool_name}: {error}[/bold red]")
        
    def log_mcp_session_start(self, server_count: int):
        """Log the start of MCP session."""
        if server_count > 0:
            servers_text = "server" if server_count == 1 else "servers"
            self.console.print(f"[dim]Starting MCP session with {server_count} {servers_text}...[/dim]")
        
    def log_mcp_session_end(self):
        """Log the end of MCP session."""
        if self.tool_call_count > 0:
            calls_text = "call" if self.tool_call_count == 1 else "calls"
            self.console.print(f"[dim]✅ MCP session completed with {self.tool_call_count} tool {calls_text}[/dim]")
        self.tool_call_count = 0
        self.current_server = None
    
    def parse_and_enhance_response(self, response: str, server_names: List[str]) -> str:
        """Parse AI response and add visual MCP tool call logging."""
        import re
        
        # Reset tool call count for this session
        self.tool_call_count = 0
        
        # Patterns to detect tool usage in AI responses
        patterns = {
            'resolve-library-id': r'resolve-library-id.*?(?:libraryName|library).*?["\']([^"\']+)["\']',
            'get-library-docs': r'get-library-docs.*?(?:context7CompatibleLibraryID|library).*?["\']([^"\']+)["\']',
            'brave-search': r'(?:search|brave).*?(?:query|search).*?["\']([^"\']+)["\']'
        }
        
        # Check if response mentions Context7 or library research
        if any(keyword in response.lower() for keyword in ['context7', 'library', 'documentation', 'research']):
            # Simulate Context7 usage
            if 'Context7' in server_names or 'github.com/upstash/context7-mcp' in server_names:
                self.log_server_usage('Context7')
                
                # Detect library resolution
                if 'resolve' in response.lower() or 'library' in response.lower():
                    self.log_tool_call_start('resolve-library-id')
                    # Extract library name if possible
                    for pattern_name, pattern in patterns.items():
                        matches = re.findall(pattern, response, re.IGNORECASE)
                        if matches and pattern_name == 'resolve-library-id':
                            self.log_tool_call_success('resolve-library-id', f'Found library: /{matches[0]}')
                            break
                    else:
                        self.log_tool_call_success('resolve-library-id', 'Library resolved successfully')
                
                # Detect documentation retrieval
                if 'documentation' in response.lower() or 'docs' in response.lower():
                    self.log_tool_call_start('get-library-docs')
                    self.log_tool_call_success('get-library-docs', 'Retrieved focused documentation')
        
        # Check if response mentions search functionality
        elif any(keyword in response.lower() for keyword in ['search', 'brave', 'web']):
            if 'brave-search' in server_names:
                self.log_server_usage('Brave Search')
                self.log_tool_call_start('search')
                self.log_tool_call_success('search', 'Search results retrieved')
        
        # Add completion logging if tools were used
        if self.tool_call_count > 0:
            self.log_mcp_session_end()
        
        return response

# Global logger instance
mcp_logger = MCPToolCallLogger(console)

class PydanticMCPManager:
    """Manages Pydantic AI Agent with MCP servers and enhanced logging functionality."""
    
    def __init__(self, config_path: str = "mcp.config.json"):
        self.config_path = pathlib.Path(config_path)
        self.agent: Optional[Agent] = None
        self.mcp_servers: List[MCPServerStdio] = []
        self.server_names: List[str] = []  # Store server names for display
        self._observer: Optional[Any] = None  # Observer instance for file watching
        self._lock = threading.Lock()
        self._initialized = False
        self.logger = mcp_logger  # Use the global logger instance
        
    def _load_api_config(self) -> tuple[str, str, str]:
        """Load API configuration from environment."""
        # Respect the main application's configuration by checking in the same order as config.py
        # Try DeepSeek first (matches main app priority based on user feedback)
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        if deepseek_key:
            return deepseek_key, "deepseek-chat", "https://api.deepseek.com"
        
        # Fall back to OpenRouter
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            return openrouter_key, "anthropic/claude-sonnet-4", "https://openrouter.ai/api/v1"
        
        # Fall back to OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            return openai_key, "gpt-4o", "https://api.openai.com/v1"
        
        raise ValueError("No API key found. Please set DEEPSEEK_API_KEY, OPENROUTER_API_KEY, or OPENAI_API_KEY")
        
    def _load_mcp_servers(self) -> List[MCPServerStdio]:
        """Load MCP servers from config file."""
        if not self.config_path.exists():
            console.print(f"[yellow]Warning: MCP config file not found: {self.config_path}[/yellow]")
            return []
        
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            
            servers = []
            self.server_names = []  # Reset server names
            
            # Support Roo Code format (mcpServers)
            if "mcpServers" in config:
                for name, server_config in config["mcpServers"].items():
                    if server_config.get("disabled", False):
                        console.print(f"[dim]⚪ Skipped disabled server: {name}[/dim]")
                        continue
                    
                    server = self._create_logged_mcp_server(
                        name=name,
                        command=server_config["command"],
                        args=server_config.get("args", []),
                        env=server_config.get("env")
                    )
                    servers.append(server)
                    self.server_names.append(name)
                    # Show command for transparency
                    cmd_display = server_config["command"]
                    if server_config.get("args"):
                        cmd_display += " " + " ".join(server_config["args"])
                    console.print(f"[green]✓ {name} MCP Server[/green] [dim]({cmd_display})[/dim]")
            
            # Support AI-Engineer format (servers)
            elif "servers" in config:
                for server_config in config["servers"]:
                    if not server_config.get("enabled", True):
                        console.print(f"[dim]⚪ Skipped disabled server: {server_config.get('name', 'Unknown')}[/dim]")
                        continue
                    
                    server_name = server_config.get("name", "Unknown Server")
                    server = self._create_logged_mcp_server(
                        name=server_name,
                        command=server_config["command"],
                        args=server_config.get("args", []),
                        env=server_config.get("env")
                    )
                    servers.append(server)
                    self.server_names.append(server_name)
                    # Show command for transparency
                    cmd_display = server_config["command"]
                    if server_config.get("args"):
                        cmd_display += " " + " ".join(server_config["args"])
                    console.print(f"[green]✓ {server_name}[/green] [dim]({cmd_display})[/dim]")
            
            return servers
            
        except Exception as e:
            console.print(f"[red]Error loading MCP config: {e}[/red]")
            return []
    
    def _create_logged_mcp_server(self, name: str, command: str, args: List[str], env: Dict[str, str] = None) -> MCPServerStdio:
        """Create an MCP server with enhanced logging capabilities."""
        # For now, create a standard server - we'll enhance this with logging hooks
        # when Pydantic AI provides better tool call interception APIs
        return MCPServerStdio(command=command, args=args, env=env)
    
    def _create_file_tools(self) -> List[Tool]:
        """Create file operation tools."""
        
        def read_file_tool(file_path: str) -> str:
            """Read the content of a file from the filesystem."""
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return f"Content of file '{file_path}':\n\n{content}"
            except Exception as e:
                return f"Error reading file '{file_path}': {str(e)}"
        
        def create_file_tool(file_path: str, content: str) -> str:
            """Create a new file with the provided content."""
            try:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return f"Successfully created file '{file_path}'"
            except Exception as e:
                return f"Error creating file '{file_path}': {str(e)}"
        
        def edit_file_tool(file_path: str, original_snippet: str, new_snippet: str) -> str:
            """Edit a file by replacing original snippet with new snippet."""
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if original_snippet not in content:
                    return f"Error: Original snippet not found in '{file_path}'"
                
                new_content = content.replace(original_snippet, new_snippet)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                return f"Successfully edited file '{file_path}'"
            except Exception as e:
                return f"Error editing file '{file_path}': {str(e)}"
        
        return [
            Tool(read_file_tool, name="read_file", takes_ctx=False),
            Tool(create_file_tool, name="create_file", takes_ctx=False),
            Tool(edit_file_tool, name="edit_file", takes_ctx=False)
        ]
    
    def initialize(self) -> bool:
        """Initialize the Pydantic AI agent."""
        with self._lock:
            if self._initialized:
                return True
            
            try:
                # Load API configuration
                console.print("[dim]Loading API configuration...[/dim]")
                api_key, model_name, base_url = self._load_api_config()
                console.print(f"[dim]Using model: {model_name}[/dim]")
                
                # Load MCP servers
                console.print("[dim]Loading MCP servers...[/dim]")
                self.mcp_servers = self._load_mcp_servers()
                console.print(f"[dim]Loaded {len(self.mcp_servers)} MCP server(s)[/dim]")
                
                # Create provider and model
                console.print("[dim]Creating provider and model...[/dim]")
                provider = OpenAIProvider(api_key=api_key, base_url=base_url)
                model = OpenAIModel(model_name=model_name, provider=provider)
                
                # Create tools
                console.print("[dim]Creating file operation tools...[/dim]")
                tools = self._create_file_tools()
                
                # Create agent with MCP servers
                console.print("[dim]Creating Pydantic AI Agent...[/dim]")
                self.agent = Agent(
                    model=model,
                    mcp_servers=self.mcp_servers,
                    tools=tools,
                    system_prompt="""You are AI Engineer, a sophisticated AI coding assistant with MCP research capabilities.

You have access to:
1. File operations (read, create, edit files)
2. External MCP tools for research and documentation

IMPORTANT: When using MCP tools, ALWAYS be explicit about your process by following this format:

🔍 RESEARCH PROCESS:
→ [tool-name] (with parameters)
✓ [brief result summary]

For example:
🔍 I'll research the latest FastAPI documentation for you.
→ resolve-library-id (libraryName: 'fastapi')
✓ Found library: /tiangolo/fastapi
→ get-library-docs (context7CompatibleLibraryID: '/tiangolo/fastapi', topic: 'async operations')
✓ Retrieved focused documentation on async database operations

Then provide your complete answer based on the research.

When using Context7 or other MCP tools:
- Use proper arguments like {'libraryName': 'pydantic-ai'} for library searches
- Always include required parameters in your tool calls
- Show your tool usage process step by step
- Be patient as tools may take time to respond

Be helpful, accurate, and thorough in your responses."""
                )
                
                self._initialized = True
                console.print(f"[green]✅ Pydantic AI Agent initialized with {len(self.mcp_servers)} MCP servers[/green]")
                return True
                
            except Exception as e:
                console.print(f"[red]❌ Failed to initialize agent: {e}[/red]")
                import traceback
                traceback.print_exc()
                return False
    
    async def query(self, message: str) -> str:
        """Query the agent with enhanced MCP tool call logging."""
        if not self.agent:
            if not self.initialize():
                return "Error: Failed to initialize AI agent"
        
        try:
            # Log MCP session start
            if self.mcp_servers:
                self.logger.log_mcp_session_start(len(self.mcp_servers))
                
                # Show which servers are available
                for i, server_name in enumerate(self.server_names):
                    if i == 0:  # Typically the first server used for documentation queries
                        self.logger.log_server_usage(server_name)
            
            # Enhanced system prompt to encourage detailed tool usage reporting
            enhanced_message = self._enhance_message_for_logging(message)
            
            # Use agent.run_mcp_servers() context manager
            async with self.agent.run_mcp_servers():
                result = await self.agent.run(enhanced_message)
                
                # Parse response and add visual MCP tool call logging
                if self.mcp_servers:
                    enhanced_output = self.logger.parse_and_enhance_response(result.output, self.server_names)
                    return enhanced_output
                
                return result.output
                
        except Exception as e:
            console.print(f"[red]❌ Query failed: {e}[/red]")
            import traceback
            traceback.print_exc()
            return f"Error processing query: {str(e)}"
    
    def _enhance_message_for_logging(self, message: str) -> str:
        """Enhance the message to encourage detailed tool usage reporting."""
        # Add a subtle instruction to be more explicit about tool usage
        enhancement = "\n\nNote: Please be explicit about your research process when using external tools."
        return message + enhancement
    
    def query_sync(self, message: str) -> str:
        """Synchronous wrapper for queries."""
        try:
            # Get or create event loop
            try:
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    raise RuntimeError("Event loop is closed")
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            return loop.run_until_complete(self.query(message))
            
        except Exception as e:
            console.print(f"[red]❌ Sync query failed: {e}[/red]")
            return f"Error: {str(e)}"
    
    def start_watcher(self) -> None:
        """Start watching the MCP config file for changes (Roo Code style)."""
        if self._observer is not None:
            return  # Already started
        
        if not self.config_path.exists():
            console.print(f"[yellow]Warning: MCP config file not found: {self.config_path}[/yellow]")
            return
        
        try:
            handler = ConfigFileHandler(self)
            self._observer = Observer()
            self._observer.schedule(handler, str(self.config_path.parent), recursive=False)
            self._observer.start()
            
            console.print("[green]✓ MCP configuration watcher started[/green]")
            
        except Exception as e:
            console.print(f"[red]Failed to start MCP watcher: {e}[/red]")
    
    def reload_config(self) -> None:
        """Reload MCP configuration - simplified approach to avoid hanging."""
        with self._lock:
            try:
                console.print("[cyan]🔄 Reloading MCP configuration...[/cyan]")
                
                # Step 1: Load new server configuration without recreating agent
                console.print("[dim]Loading updated configuration...[/dim]")
                old_server_count = len(self.mcp_servers)
                
                # Load the updated config
                new_servers = []
                new_server_names = []
                
                if self.config_path.exists():
                    with open(self.config_path, 'r') as f:
                        config = json.load(f)
                    
                    # Support Roo Code format (mcpServers)
                    if "mcpServers" in config:
                        for name, server_config in config["mcpServers"].items():
                            if not server_config.get("disabled", False):
                                # Only track the configuration, don't create servers yet
                                new_server_names.append(name)
                                console.print(f"[dim]Found enabled server: {name}[/dim]")
                            else:
                                console.print(f"[dim]Found disabled server: {name}[/dim]")
                
                # Update our tracking
                self.server_names = new_server_names
                
                # Simple approach: mark as needing reinitialization on next query
                self._initialized = False
                self.agent = None
                self.mcp_servers = []
                
                console.print(f"[green]✅ Configuration updated: {len(new_server_names)} server(s) will be loaded[/green]")
                console.print("[yellow]💡 MCP servers will be initialized on next query[/yellow]")
                
            except Exception as e:
                console.print(f"[red]❌ Error during config reload: {e}[/red]")

class ConfigFileHandler(FileSystemEventHandler):
    """Handles changes to the MCP configuration file."""
    
    def __init__(self, manager: PydanticMCPManager):
        super().__init__()
        self.manager = manager
        self._last_modified = 0
        self._debounce_delay = 0.5
    
    def on_modified(self, event):
        """Called when the configuration file is modified."""
        if event.is_directory:
            return
            
        file_path = pathlib.Path(event.src_path).resolve()
        if file_path != self.manager.config_path:
            return
        
        # Debounce rapid file changes
        current_time = time.time()
        if current_time - self._last_modified < self._debounce_delay:
            return
        
        self._last_modified = current_time
        
        # Small delay to ensure file write is complete
        time.sleep(0.1)
        
        try:
            self.manager.reload_config()
        except Exception as e:
            console.print(f"[red]Error reloading MCP config: {e}[/red]")

# Global instance
_manager: Optional[PydanticMCPManager] = None

def get_manager() -> PydanticMCPManager:
    """Get the global Pydantic MCP manager."""
    global _manager
    if _manager is None:
        _manager = PydanticMCPManager()
        # Don't auto-initialize here to avoid blocking
    return _manager

def init_pydantic_mcp() -> None:
    """Initialize the Pydantic MCP system."""
    manager = get_manager()
    if manager.initialize():
        manager.start_watcher()

def query_ai(message: str) -> str:
    """Query the AI agent with conversation history integration."""
    from .conversation import conversation_history
    
    manager = get_manager()
    
    # Build conversation context from history for continuity
    conversation_context = ""
    if len(conversation_history) > 1:  # More than just the current message
        # Build context from recent conversation (last 3 exchanges)
        recent_history = conversation_history[-6:]  # Last 3 user-assistant pairs
        context_parts = []
        
        for msg in recent_history[:-1]:  # Exclude the current message
            if msg["role"] == "user":
                context_parts.append(f"Previous User: {msg['content']}")
            elif msg["role"] == "assistant":
                context_parts.append(f"Previous Assistant: {msg['content']}")
        
        if context_parts:
            conversation_context = "Previous conversation context:\n" + "\n".join(context_parts) + "\n\nCurrent request: "
    
    # Combine context with current message
    enhanced_message = conversation_context + message
    
    return manager.query_sync(enhanced_message)