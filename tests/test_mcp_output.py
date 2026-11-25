"""Tests for what the MCP path prints around the agent reply."""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from types import SimpleNamespace

from rich.text import Text

from AI_engineer import api_client
from AI_engineer import pydantic_mcp_integration as pmi
from AI_engineer.conversation import conversation_history

REPLY = "See the library docs: use Dict[str, Any] here."


class FakeAgent:
    """Stands in for the Pydantic AI agent: no model, no MCP server."""

    def __init__(self) -> None:
        self.messages: list[str] = []

    @asynccontextmanager
    async def run_mcp_servers(self):
        yield

    async def run(self, message: str):
        self.messages.append(message)
        return SimpleNamespace(output=REPLY)


class TestMcpOutput:
    def test_query_returns_the_reply_without_tool_call_lines(self) -> None:
        manager = pmi.PydanticMCPManager()
        manager.agent = FakeAgent()
        manager.mcp_servers = [object()]
        manager.server_names = ["Context7", "brave-search"]
        with pmi.console.capture() as captured:
            output = asyncio.run(manager.query("explain the fastapi docs"))
        printed = Text.from_ansi(captured.get()).plain
        assert output == REPLY
        assert manager.agent.messages == ["explain the fastapi docs"]
        assert printed == "Starting MCP session with 1 server..."

    def test_mcp_reply_is_printed_without_a_completion_claim(self, monkeypatch) -> None:
        monkeypatch.setattr(pmi, "query_ai", lambda message: REPLY)
        start = len(conversation_history)
        try:
            with api_client.console.capture() as captured:
                api_client._handle_mcp_enhanced_query("explain the fastapi docs")
        finally:
            del conversation_history[start:]
        printed = Text.from_ansi(captured.get()).plain
        assert printed == REPLY
