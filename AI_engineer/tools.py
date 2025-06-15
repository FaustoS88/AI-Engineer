#!/usr/bin/env python3

# --------------------------------------------------------------------------------
# Function Calling Tools Definitions
# --------------------------------------------------------------------------------

# Base AI-Engineer tools for file operations
base_tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the content of a single file from the filesystem",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to read (relative or absolute)",
                    }
                },
                "required": ["file_path"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_multiple_files",
            "description": "Read the content of multiple files from the filesystem",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Array of file paths to read (relative or absolute)",
                    }
                },
                "required": ["file_paths"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_file",
            "description": "Create a new file or overwrite an existing file with the provided content",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path where the file should be created",
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file",
                    }
                },
                "required": ["file_path", "content"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_multiple_files",
            "description": "Create multiple files at once",
            "parameters": {
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string"},
                                "content": {"type": "string"}
                            },
                            "required": ["path", "content"]
                        },
                        "description": "Array of files to create with their paths and content",
                    }
                },
                "required": ["files"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "Edit an existing file by replacing a specific snippet with new content",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to edit",
                    },
                    "original_snippet": {
                        "type": "string",
                        "description": "The exact text snippet to find and replace",
                    },
                    "new_snippet": {
                        "type": "string",
                        "description": "The new text to replace the original snippet with",
                    }
                },
                "required": ["file_path", "original_snippet", "new_snippet"]
            },
        }
    }
]

def get_mcp_tools_openai_format():
    """Get MCP tools in OpenAI function calling format using the new Pydantic AI MCP integration."""
    try:
        from .pydantic_mcp_integration import get_manager
        
        # Get the Pydantic MCP manager
        manager = get_manager()
        
        # Initialize if not already initialized
        if not manager._initialized:
            manager.initialize()
        
        # Now check if we have servers
        if not manager.mcp_servers:
            # This is fine - means no MCP servers are configured, not an error
            return []
        
        # The new system doesn't need to extract raw schemas - Pydantic AI handles this
        # We'll return an empty list for now since the new system uses Pydantic AI tools directly
        print(f"ℹ️ Using new Pydantic AI MCP integration with {len(manager.mcp_servers)} server(s) - tools are handled directly by agent")
        return []
        
    except Exception as e:
        print(f"❌ Failed to get MCP tools: {e}")
        import traceback
        traceback.print_exc()
        return []

def _is_valid_openai_function_name(name: str) -> bool:
    """Check if a function name meets OpenAI's requirements."""
    import re
    # OpenAI function names should use only: letters, numbers, underscores (no hyphens)
    # This matches our sanitization approach
    if not name or len(name) > 64:
        return False
    return bool(re.match(r'^[a-zA-Z0-9_]+$', name))

def get_all_tools():
    """Get all tools including base tools and MCP tools."""
    all_tools = base_tools.copy()
    mcp_tools = get_mcp_tools_openai_format()
    all_tools.extend(mcp_tools)
    return all_tools

# Dynamic tools that includes MCP tools
tools = get_all_tools()

def refresh_tools():
    """Refresh the tools list to include newly loaded MCP tools."""
    global tools
    tools = get_all_tools()