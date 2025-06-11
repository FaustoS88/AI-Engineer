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

def execute_function_call_dict(tool_call_dict) -> str:
    """Execute a function call from a dictionary format and return the result as a string."""
    try:
        function_name = tool_call_dict["function"]["name"]
        arguments = json.loads(tool_call_dict["function"]["arguments"])
        
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
    """Stream response from OpenAI API with recursive function calling support."""
    # Get the current client
    client = get_client()
    if not client:
        return {"error": "No valid API client available. Please check your API keys."}
    
    current_model = get_current_model()
    
    # Add the user message to conversation history
    conversation_history.append({"role": "user", "content": user_message})
    
    # Trim conversation history if it's getting too long
    trim_conversation_history()

    try:
        # Start the recursive function calling loop
        return _recursive_function_calling_loop(client, current_model)

    except Exception as e:
        error_msg = f"API error: {str(e)}"
        console.print(f"\n[bold red]❌ {error_msg}[/bold red]")
        return {"error": error_msg}


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
    
    while iteration < max_iterations:
        iteration += 1
        console.print(f"\n[dim]🔄 Iteration {iteration}[/dim]")
        
        # Prepare request parameters
        request_params = {
            "model": current_model,
            "messages": conversation_history,
            "tools": tools,
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
            # Handle reasoning content if available (only for DeepSeek models)
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
                # Important: When there are tool calls, content should be None or empty
                if not final_content:
                    assistant_message["content"] = None
                    
                assistant_message["tool_calls"] = formatted_tool_calls
                conversation_history.append(assistant_message)
                
                # Execute tool calls and add results immediately
                console.print(f"\n[bold bright_cyan]⚡ Executing {len(formatted_tool_calls)} function call(s)...[/bold bright_cyan]")
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
                        conversation_history.append({
                            "role": "tool",
                            "tool_call_id": tool_call["id"],
                            "content": f"Error: {str(e)}"
                        })
                
                # Continue the loop to check for more function calls
                console.print(f"[dim]✅ Function calls completed. Checking for additional actions...[/dim]")
                continue
        else:
            # No tool calls, store the response and exit the loop
            conversation_history.append(assistant_message)
            console.print(f"[dim]✅ Task completed after {iteration} iteration(s)[/dim]")
            break
    
    if iteration >= max_iterations:
        console.print(f"\n[yellow]⚠️  Reached maximum iterations ({max_iterations}). Task may be incomplete.[/yellow]")
    
    return {"success": True}