"""Tests for tools module — function name validation."""

from __future__ import annotations

import pytest

from AI_engineer.tools import _is_valid_openai_function_name


class TestIsValidOpenAIFunctionName:
    @pytest.mark.parametrize(
        "name",
        ["read_file", "create_file", "my_tool_123", "a", "A_B_C"],
    )
    def test_valid_names(self, name: str) -> None:
        assert _is_valid_openai_function_name(name) is True

    def test_empty_string(self) -> None:
        assert _is_valid_openai_function_name("") is False

    def test_too_long(self) -> None:
        assert _is_valid_openai_function_name("a" * 65) is False

    def test_max_length_ok(self) -> None:
        assert _is_valid_openai_function_name("a" * 64) is True

    @pytest.mark.parametrize(
        "name",
        ["read-file", "my tool", "fn()", "hello.world", "name@host"],
    )
    def test_invalid_chars(self, name: str) -> None:
        assert _is_valid_openai_function_name(name) is False
