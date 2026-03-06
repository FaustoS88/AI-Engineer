"""Tests for error detection — file type checks and supported extensions."""

from __future__ import annotations

import pytest

from AI_engineer.error_detection import (
    get_supported_extensions,
    is_javascript_file,
    is_python_file,
    is_supported_file,
    is_typescript_file,
)


# ---------------------------------------------------------------------------
# File type detection
# ---------------------------------------------------------------------------

class TestIsPythonFile:
    @pytest.mark.parametrize("path", ["main.py", "src/agent.py", "/tmp/test.py"])
    def test_python_files(self, path: str) -> None:
        assert is_python_file(path) is True

    @pytest.mark.parametrize("path", ["main.js", "file.ts", "readme.md", "config.yaml"])
    def test_non_python_files(self, path: str) -> None:
        assert is_python_file(path) is False


class TestIsJavaScriptFile:
    @pytest.mark.parametrize("path", ["app.js", "Component.jsx", "src/index.js"])
    def test_js_files(self, path: str) -> None:
        assert is_javascript_file(path) is True

    @pytest.mark.parametrize("path", ["app.ts", "main.py", "style.css"])
    def test_non_js_files(self, path: str) -> None:
        assert is_javascript_file(path) is False


class TestIsTypeScriptFile:
    @pytest.mark.parametrize("path", ["app.ts", "Component.tsx", "src/index.ts"])
    def test_ts_files(self, path: str) -> None:
        assert is_typescript_file(path) is True

    @pytest.mark.parametrize("path", ["app.js", "main.py", "style.css"])
    def test_non_ts_files(self, path: str) -> None:
        assert is_typescript_file(path) is False


# ---------------------------------------------------------------------------
# Supported extensions
# ---------------------------------------------------------------------------

class TestSupportedExtensions:
    def test_includes_python(self) -> None:
        assert ".py" in get_supported_extensions()

    def test_includes_js(self) -> None:
        exts = get_supported_extensions()
        assert ".js" in exts
        assert ".jsx" in exts

    def test_includes_ts(self) -> None:
        exts = get_supported_extensions()
        assert ".ts" in exts
        assert ".tsx" in exts


class TestIsSupportedFile:
    @pytest.mark.parametrize(
        "path",
        ["main.py", "app.js", "App.jsx", "index.ts", "Component.tsx"],
    )
    def test_supported_files(self, path: str) -> None:
        assert is_supported_file(path) is True

    @pytest.mark.parametrize(
        "path",
        ["readme.md", "config.yaml", "Makefile", "style.css", "image.png"],
    )
    def test_unsupported_files(self, path: str) -> None:
        assert is_supported_file(path) is False
