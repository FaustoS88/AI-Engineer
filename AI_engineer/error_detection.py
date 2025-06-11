#!/usr/bin/env python3

"""Automatic error detection utilities.

This module provides helper functions to run linters on source files and
return diagnostic messages. Supports Python, JavaScript, and TypeScript files
with their respective linters (flake8, eslint, tsc).
"""

from pathlib import Path
import subprocess
import json


def is_python_file(file_path: str) -> bool:
    """Return ``True`` if ``file_path`` points to a Python source file."""
    return file_path.endswith(".py")


def is_javascript_file(file_path: str) -> bool:
    """Return ``True`` if ``file_path`` points to a JavaScript source file."""
    return file_path.endswith((".js", ".jsx"))


def is_typescript_file(file_path: str) -> bool:
    """Return ``True`` if ``file_path`` points to a TypeScript source file."""
    return file_path.endswith((".ts", ".tsx"))


def run_flake8(file_path: str) -> str:
    """Run ``flake8`` on ``file_path`` and return its diagnostic output."""
    try:
        result = subprocess.run(
            ["flake8", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            timeout=10,
        )
        return result.stdout.strip()
    except Exception as e:  # pragma: no cover - best effort
        return f"[Linter Error] Could not check file {file_path}: {e}"


def run_eslint(file_path: str) -> str:
    """Run ``eslint`` on ``file_path`` and return its diagnostic output."""
    try:
        # Try to run eslint with JSON format for better parsing
        result = subprocess.run(
            ["npx", "eslint", "--format", "compact", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            timeout=15,
        )
        
        # ESLint returns non-zero exit code when issues are found
        output = result.stdout.strip()
        if output:
            return output
        
        # If no stdout but stderr, it might be a configuration issue
        if result.stderr.strip():
            return f"[ESLint Config] {result.stderr.strip()}"
            
        return ""  # No issues found
        
    except FileNotFoundError:
        return "[ESLint Error] ESLint not found. Install with: npm install -g eslint"
    except Exception as e:
        return f"[Linter Error] Could not check file {file_path}: {e}"


def run_typescript_check(file_path: str) -> str:
    """Run TypeScript compiler check on ``file_path`` and return diagnostics."""
    try:
        # Use tsc --noEmit to check for type errors without generating files
        result = subprocess.run(
            ["npx", "tsc", "--noEmit", "--skipLibCheck", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            timeout=15,
        )
        
        # Combine stdout and stderr for comprehensive error reporting
        output = ""
        if result.stdout.strip():
            output += result.stdout.strip()
        if result.stderr.strip():
            if output:
                output += "\n"
            output += result.stderr.strip()
            
        return output
        
    except FileNotFoundError:
        return "[TypeScript Error] TypeScript compiler not found. Install with: npm install -g typescript"
    except Exception as e:
        return f"[Linter Error] Could not check file {file_path}: {e}"


def run_linter_auto(file_path: str) -> str:
    """Run the appropriate linter for ``file_path`` and return diagnostics."""
    path = Path(file_path)
    file_name = path.name
    
    if is_python_file(file_name):
        return run_flake8(str(path))
    elif is_javascript_file(file_name):
        return run_eslint(str(path))
    elif is_typescript_file(file_name):
        # For TypeScript files, run both TypeScript compiler and ESLint
        ts_output = run_typescript_check(str(path))
        eslint_output = run_eslint(str(path))
        
        combined_output = ""
        if ts_output.strip():
            combined_output += f"TypeScript Compiler:\n{ts_output}"
        if eslint_output.strip():
            if combined_output:
                combined_output += "\n\n"
            combined_output += f"ESLint:\n{eslint_output}"
            
        return combined_output
    
    # No linter available for this file type
    return ""


def get_supported_extensions() -> list:
    """Return a list of file extensions supported by the error detection system."""
    return [".py", ".js", ".jsx", ".ts", ".tsx"]


def is_supported_file(file_path: str) -> bool:
    """Return ``True`` if the file type is supported by the error detection system."""
    return any(file_path.endswith(ext) for ext in get_supported_extensions())

