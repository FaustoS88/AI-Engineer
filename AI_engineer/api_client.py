#!/usr/bin/env python3

import json
import time

from .config import (
    get_client, console, get_current_model,
    get_provider_headers, get_provider_extra_body, supports_reasoning
)
from .tools import tools
from .conversation import conversation_history, trim_conversation_history
from .file_operations import (
    read_local_file, create_file, normalize_path, ensure_file_in_context,
    apply_diff_edit
)
from .error_detection import run_linter_auto, is_supported_file

# --------------------------------------------------------------------------------
# OpenAI API Integration and Function Execution
# --------------------------------------------------------------------------------

# Pydantic AI agent handles MCP tool execution
def execute_mcp_tool(function_name: str, arguments: dict) -> str:
    """Legacy MCP tool execution - now handled by Pydantic AI agent."""
    return f"Error: Legacy MCP tool execution disabled. Using Pydantic AI agent instead."

def execute_function_call_dict(tool_call_dict) -> str:
    """Execute a function call from a dictionary format and return the result as a string."""
    try:
        function_name = tool_call_dict["function"]["name"]
        arguments = json.loads(tool_call_dict["function"]["arguments"])
        
        # Check if this is an MCP tool (contains server prefix)
        if "_" in function_name and function_name not in ["read_file", "create_file", "edit_file", "read_multiple_files", "create_multiple_files"]:
            return execute_mcp_tool(function_name, arguments)
        
        if function_name == "read_file":
            file_path = arguments["file_path"]
            normalized_path = normalize_path(file_path)
            content = read_local_file(normalized_path, with_diagnostics=True)
            
            # Add automatic error detection for supported files (Python, JS, TS)
            error_info = ""
            if is_supported_file(normalized_path):
                linter_output = run_linter_auto(normalized_path)
                if linter_output.strip():
                    error_info = f"\n\n🔍 LINTER DIAGNOSTICS:\n{linter_output}\n\n⚠️  ISSUES DETECTED - Please fix these errors/warnings!"
            
            return f"Content of file '{normalized_path}':\n\n{content}{error_info}"
            
        elif function_name == "read_multiple_files":
            file_paths = arguments["file_paths"]
            results = []
            for file_path in file_paths:
                try:
                    normalized_path = normalize_path(file_path)
                    content = read_local_file(normalized_path, with_diagnostics=True)
                    results.append(f"Content of file '{normalized_path}':\n\n{content}")
                except OSError as e:
                    results.append(f"Error reading '{file_path}': {e}")
            return "\n\n" + "="*50 + "\n\n".join(results)
            
        elif function_name == "create_file":
            file_path = arguments["file_path"]
            content = arguments["content"]
            create_file(file_path, content)
            
            # Run error detection on newly created files (Python, JS, TS)
            error_info = ""
            if is_supported_file(file_path):
                linter_output = run_linter_auto(file_path)
                if linter_output.strip():
                    error_info = f"\n\n🔍 LINTER DIAGNOSTICS for new file:\n{linter_output}\n\n⚠️  ISSUES DETECTED - Consider fixing these errors/warnings!"
            
            return f"Successfully created file '{file_path}'{error_info}"
            
        elif function_name == "create_multiple_files":
            files = arguments["files"]
            created_files = []
            for file_info in files:
                create_file(file_info["path"], file_info["content"])
                created_files.append(file_info["path"])
            return f"Successfully created {len(created_files)} files: {', '.join(created_files)}"
            
        elif function_name == "edit_file":
            file_path = arguments["file_path"]
            original_snippet = arguments["original_snippet"]
            new_snippet = arguments["new_snippet"]
            
            # Ensure file is in context first
            if not ensure_file_in_context(file_path):
                return f"Error: Could not read file '{file_path}' for editing"
            
            apply_diff_edit(file_path, original_snippet, new_snippet)
            
            # Run error detection on edited files (Python, JS, TS)
            error_info = ""
            if is_supported_file(file_path):
                linter_output = run_linter_auto(file_path)
                if linter_output.strip():
                    error_info = f"\n\n🔍 LINTER DIAGNOSTICS after edit:\n{linter_output}\n\n⚠️  ISSUES DETECTED - Consider fixing these errors/warnings!"
            
            return f"Successfully edited file '{file_path}'{error_info}"
            
        else:
            return f"Unknown function: {function_name}"
            
    except Exception as e:
        return f"Error executing {function_name}: {str(e)}"

def execute_function_call(tool_call) -> str:
    """Execute a function call and return the result as a string."""
    try:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        # Check if this is an MCP tool (contains server prefix)
        if "_" in function_name and function_name not in ["read_file", "create_file", "edit_file", "read_multiple_files", "create_multiple_files"]:
            return execute_mcp_tool(function_name, arguments)
        
        if function_name == "read_file":
            file_path = arguments["file_path"]
            normalized_path = normalize_path(file_path)
            content = read_local_file(normalized_path, with_diagnostics=True)
            
            # Add automatic error detection for supported files (Python, JS, TS)
            error_info = ""
            if is_supported_file(normalized_path):
                linter_output = run_linter_auto(normalized_path)
                if linter_output.strip():
                    error_info = f"\n\n🔍 LINTER DIAGNOSTICS:\n{linter_output}\n\n⚠️  ISSUES DETECTED - Please fix these errors/warnings!"
            
            return f"Content of file '{normalized_path}':\n\n{content}{error_info}"
            
        elif function_name == "read_multiple_files":
            file_paths = arguments["file_paths"]
            results = []
            for file_path in file_paths:
                try:
                    normalized_path = normalize_path(file_path)
                    content = read_local_file(normalized_path, with_diagnostics=True)
                    results.append(f"Content of file '{normalized_path}':\n\n{content}")
                except OSError as e:
                    results.append(f"Error reading '{file_path}': {e}")
            return "\n\n" + "="*50 + "\n\n".join(results)
            
        elif function_name == "create_file":
            file_path = arguments["file_path"]
            content = arguments["content"]
            create_file(file_path, content)
            
            # Run error detection on newly created files (Python, JS, TS)
            error_info = ""
            if is_supported_file(file_path):
                linter_output = run_linter_auto(file_path)
                if linter_output.strip():
                    error_info = f"\n\n🔍 LINTER DIAGNOSTICS for new file:\n{linter_output}\n\n⚠️  ISSUES DETECTED - Consider fixing these errors/warnings!"
            
            return f"Successfully created file '{file_path}'{error_info}"
            
        elif function_name == "create_multiple_files":
            files = arguments["files"]
            created_files = []
            for file_info in files:
                create_file(file_info["path"], file_info["content"])
                created_files.append(file_info["path"])
            return f"Successfully created {len(created_files)} files: {', '.join(created_files)}"
            
        elif function_name == "edit_file":
            file_path = arguments["file_path"]
            original_snippet = arguments["original_snippet"]
            new_snippet = arguments["new_snippet"]
            
            # Ensure file is in context first
            if not ensure_file_in_context(file_path):
                return f"Error: Could not read file '{file_path}' for editing"
            
            apply_diff_edit(file_path, original_snippet, new_snippet)
            
            # Run error detection on edited files (Python, JS, TS)
            error_info = ""
            if is_supported_file(file_path):
                linter_output = run_linter_auto(file_path)
                if linter_output.strip():
                    error_info = f"\n\n🔍 LINTER DIAGNOSTICS after edit:\n{linter_output}\n\n⚠️  ISSUES DETECTED - Consider fixing these errors/warnings!"
            
            return f"Successfully edited file '{file_path}'{error_info}"
            
        else:
            return f"Unknown function: {function_name}"
            
    except Exception as e:
        return f"Error executing {function_name}: {str(e)}"

def stream_openai_response(user_message: str):
    """
    Primary function for AI responses using recursive function calling system.
    Uses MCP/Pydantic AI intelligently as enhancement when library research is needed.
    """
    client = get_client()
    current_model = get_current_model()
    
    # Add user message to conversation history
    conversation_history.append({"role": "user", "content": user_message})
    trim_conversation_history()
    
    # Intelligent approach selection: Check if user needs library research or documentation
    needs_mcp = _should_use_mcp(user_message)
    
    if needs_mcp:
        console.print("\n[bold bright_blue]🤖 AI Engineer (with MCP Research)>[/bold bright_blue]")
        return _handle_mcp_enhanced_query(user_message)
    else:
        # Use proven recursive function calling system by default
        return _recursive_function_calling_loop(client, current_model)

def _should_use_mcp(user_message: str) -> bool:
    """
    Determine if the query needs MCP tools for library research, documentation, or external services.
    """
    mcp_keywords = [
        # Research & Documentation
        "documentation", "docs", "library", "package", "framework", "api reference",
        "how to use", "tutorial", "guide", "example", "context7", "research",
        # Crypto & Trading (CCXT server)
        "price", "btc", "bitcoin", "ethereum", "eth", "crypto", "cryptocurrency",
        "trading", "exchange", "binance", "coinbase", "kraken", "market", "ccxt", "cctx",
        # MCP Server mentions
        "mcp server", "mcp tool", "use mcp", "fetch", "get price", "market data"
    ]
    
    message_lower = user_message.lower()
    return any(keyword in message_lower for keyword in mcp_keywords)

def _handle_mcp_enhanced_query(user_message: str):
    """
    Handle queries that need MCP tools with fallback to recursive calling.
    """
    try:
        from .pydantic_mcp_integration import query_ai
        
        # Use MCP for research/documentation queries
        response = query_ai(user_message)
        
        # Add the assistant's response to conversation history
        conversation_history.append({"role": "assistant", "content": response})
        
        # Stream the response character by character for the UI effect
        for char in response:
            console.print(char, end="")
        
        console.print()  # New line after streaming
        console.print(f"[dim]✅ Task completed using MCP research tools[/dim]")
        
        return {"success": True}
        
    except Exception as e:
        console.print(f"\n[yellow]⚠️  MCP fallback failed: {str(e)}[/yellow]")
        console.print("[cyan]🔄 Falling back to recursive function calling...[/cyan]")
        
        # Fallback to recursive calling system
        client = get_client()
        current_model = get_current_model()
        return _recursive_function_calling_loop(client, current_model)


def _is_trivial_iteration(tool_calls):
    """
    Detect if the current iteration involves only trivial edits (spacing, formatting, etc.)
    to prevent infinite loops on minor issues.
    """
    if not tool_calls:
        return False
    
    trivial_keywords = [
        "blank line", "spacing", "whitespace", "indentation",
        "extra blank", "remove blank", "add blank", "pep 8",
        "two blank lines", "blank lines between", "trailing whitespace"
    ]
    
    for tool_call in tool_calls:
        if tool_call['function']['name'] == 'edit_file':
            try:
                # Check if the arguments suggest trivial formatting changes
                args = json.loads(tool_call['function']['arguments'])
                original = args.get('original_snippet', '').lower()
                new = args.get('new_snippet', '').lower()
                
                # If the content is very similar and involves spacing/formatting
                if len(original.strip()) > 0 and len(new.strip()) > 0:
                    # Check if changes are only whitespace/formatting
                    original_no_space = ''.join(original.split())
                    new_no_space = ''.join(new.split())
                    
                    if original_no_space == new_no_space:  # Only whitespace changes
                        return True
                        
                # Check for trivial keyword patterns
                combined_text = (original + ' ' + new).lower()
                if any(keyword in combined_text for keyword in trivial_keywords):
                    return True
                    
            except (json.JSONDecodeError, KeyError):
                continue
    
    return False


def _recursive_function_calling_loop(client, current_model, max_iterations=10):
    """
    Recursive function calling loop that continues until no more function calls are needed.
    
    Args:
        client: The API client
        current_model: Current model being used
        max_iterations: Maximum number of iterations to prevent infinite loops
    
    Returns:
        dict: Success or error response
    """
    iteration = 0
    consecutive_trivial_iterations = 0  # Track trivial edits to prevent infinite loops
    
    while iteration < max_iterations:
        iteration += 1
        console.print(f"\n[dim]🔄 Iteration {iteration}[/dim]")
        
        # Use the proper tools from the tools module for recursive function calling
        current_tools = tools
        
        # Prepare request parameters
        request_params = {
            "model": current_model,
            "messages": conversation_history,
            "tools": current_tools,
            "max_completion_tokens": 64000,
            "stream": True
        }
        
        # Add provider-specific headers and extra body for OpenRouter
        extra_headers = get_provider_headers()
        extra_body = get_provider_extra_body()
        
        if extra_headers:
            request_params["extra_headers"] = extra_headers
        if extra_body:
            request_params["extra_body"] = extra_body

        stream = client.chat.completions.create(**request_params)

        if iteration == 1:
            console.print("\n[bold bright_blue]🤖 AI Engineer>[/bold bright_blue]")
        else:
            console.print("\n[bold bright_blue]🔄 Continuing...[/bold bright_blue]")
            
        reasoning_started = False
        reasoning_content = ""
        final_content = ""
        tool_calls = []

        for chunk in stream:
            # Handle reasoning content if available (mostly for DeepSeek R1 model)
            if (supports_reasoning() and
                hasattr(chunk.choices[0].delta, 'reasoning_content') and
                chunk.choices[0].delta.reasoning_content):
                if not reasoning_started:
                    console.print("\n[bold blue]💭 Reasoning:[/bold blue]")
                    reasoning_started = True
                console.print(chunk.choices[0].delta.reasoning_content, end="")
                reasoning_content += chunk.choices[0].delta.reasoning_content
            elif chunk.choices[0].delta.content:
                if reasoning_started:
                    console.print("\n")  # Add spacing after reasoning
                    console.print("\n[bold bright_blue]🤖 Assistant>[/bold bright_blue] ", end="")
                    reasoning_started = False
                final_content += chunk.choices[0].delta.content
                console.print(chunk.choices[0].delta.content, end="")
            elif chunk.choices[0].delta.tool_calls:
                # Handle tool calls
                for tool_call_delta in chunk.choices[0].delta.tool_calls:
                    if tool_call_delta.index is not None:
                        # Ensure we have enough tool_calls
                        while len(tool_calls) <= tool_call_delta.index:
                            tool_calls.append({
                                "id": "",
                                "type": "function",
                                "function": {"name": "", "arguments": ""}
                            })
                        
                        if tool_call_delta.id:
                            tool_calls[tool_call_delta.index]["id"] = tool_call_delta.id
                        if tool_call_delta.function:
                            if tool_call_delta.function.name:
                                tool_calls[tool_call_delta.index]["function"]["name"] += tool_call_delta.function.name
                            if tool_call_delta.function.arguments:
                                tool_calls[tool_call_delta.index]["function"]["arguments"] += tool_call_delta.function.arguments

        console.print()  # New line after streaming

        # Store the assistant's response in conversation history
        assistant_message = {
            "role": "assistant",
            "content": final_content if final_content else None
        }
        
        if tool_calls:
            # Convert our tool_calls format to the expected format
            formatted_tool_calls = []
            
            for i, tc in enumerate(tool_calls):
                if tc["function"]["name"]:  # Only add if we have a function name
                    # Ensure we have a valid tool call ID
                    tool_id = tc["id"] if tc["id"] else f"call_{i}_{int(time.time() * 1000)}"
                    
                    formatted_tool_calls.append({
                        "id": tool_id,
                        "type": "function",
                        "function": {
                            "name": tc["function"]["name"],
                            "arguments": tc["function"]["arguments"]
                        }
                    })
            
            if formatted_tool_calls:
                # CRITICAL: OpenAI requires content=None when tool_calls are present
                # But we keep the explanatory text for the user experience
                user_explanation = final_content if final_content and final_content.strip() else None
                assistant_message["content"] = None  # Always None when tool_calls present
                    
                assistant_message["tool_calls"] = formatted_tool_calls
                conversation_history.append(assistant_message)
                
                # Show user explanation if it existed (for user experience)
                if user_explanation:
                    console.print(f"\n{user_explanation}")
                
                # Execute tool calls and add results immediately
                console.print(f"\n[bold bright_cyan]⚡ Executing {len(formatted_tool_calls)} function call(s)...[/bold bright_cyan]")
                
                # Check if these are trivial edits (spacing, formatting only)
                is_trivial_iteration = _is_trivial_iteration(formatted_tool_calls)
                if is_trivial_iteration:
                    consecutive_trivial_iterations += 1
                else:
                    consecutive_trivial_iterations = 0
                
                # Stop if we've had too many consecutive trivial iterations
                if consecutive_trivial_iterations >= 3:
                    console.print(f"[yellow]⚠️  Stopping after {consecutive_trivial_iterations} consecutive trivial edits to prevent infinite loop.[/yellow]")
                    console.print(f"[dim]✅ Task completed with minor formatting variations after {iteration} iteration(s)[/dim]")
                    break
                
                for tool_call in formatted_tool_calls:
                    console.print(f"[bright_blue]→ {tool_call['function']['name']}[/bright_blue]")
                    
                    try:
                        result = execute_function_call_dict(tool_call)
                        
                        # Add tool result to conversation immediately
                        tool_response = {
                            "role": "tool",
                            "tool_call_id": tool_call["id"],
                            "content": result
                        }
                        conversation_history.append(tool_response)
                    except Exception as e:
                        console.print(f"[red]Error executing {tool_call['function']['name']}: {e}[/red]")
                        # Still need to add a tool response even on error
                        error_response = {
                            "role": "tool",
                            "tool_call_id": tool_call["id"],
                            "content": f"Error: {str(e)}"
                        }
                        conversation_history.append(error_response)
                
                # Continue the loop to check for more function calls
                console.print(f"[dim]✅ Function calls completed. Checking for additional actions...[/dim]")
                continue
        else:
            # No tool calls, store the response and exit the loop
            # CRITICAL FIX: Ensure assistant messages always have content or tool_calls
            has_content = assistant_message["content"] is not None and assistant_message["content"].strip()
            if not has_content:
                assistant_message["content"] = "I have completed the analysis."
            
            conversation_history.append(assistant_message)
            console.print(f"[dim]✅ Task completed after {iteration} iteration(s)[/dim]")
            break
    
    if iteration >= max_iterations:
        console.print(f"\n[yellow]⚠️  Reached maximum iterations ({max_iterations}). Task may be incomplete.[/yellow]")
    
    return {"success": True}