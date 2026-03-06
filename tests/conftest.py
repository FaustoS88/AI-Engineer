"""Shared test configuration.

The AI_engineer package __init__.py eagerly imports heavy modules (MCP,
pydantic-ai) that require optional dependencies. We pre-load the lightweight
submodules before the package init runs so tests can import them directly.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

# Ensure the repo root is on sys.path so individual submodules can be found
_repo_root = Path(__file__).resolve().parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

# Stub out pydantic_ai.mcp before anything touches it — this prevents the
# ImportError cascade from AI_engineer.__init__ → config → pydantic_mcp_integration
if "pydantic_ai.mcp" not in sys.modules:
    sys.modules["pydantic_ai.mcp"] = MagicMock()
