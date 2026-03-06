"""Tests for providers module — model configs, provider configs, lookups."""

from __future__ import annotations

import pytest

from AI_engineer.providers import (
    DEFAULT_MODEL,
    MODELS,
    PROVIDERS,
    ModelConfig,
    ProviderConfig,
    get_all_models,
    get_model_config,
    get_models_by_provider,
    get_provider_config,
    is_valid_model,
)


# ---------------------------------------------------------------------------
# ModelConfig dataclass
# ---------------------------------------------------------------------------

class TestModelConfig:
    def test_required_fields(self) -> None:
        m = ModelConfig(name="test", provider="p", display_name="Test")
        assert m.name == "test"
        assert m.provider == "p"
        assert m.display_name == "Test"

    def test_default_reasoning(self) -> None:
        m = ModelConfig(name="x", provider="p", display_name="X")
        assert m.supports_reasoning is False

    def test_default_max_tokens(self) -> None:
        m = ModelConfig(name="x", provider="p", display_name="X")
        assert m.max_tokens is None

    def test_reasoning_flag(self) -> None:
        m = ModelConfig(name="x", provider="p", display_name="X", supports_reasoning=True)
        assert m.supports_reasoning is True


# ---------------------------------------------------------------------------
# ProviderConfig dataclass
# ---------------------------------------------------------------------------

class TestProviderConfig:
    def test_required_fields(self) -> None:
        p = ProviderConfig(name="Test", base_url="https://example.com", api_key_env="KEY")
        assert p.name == "Test"
        assert p.base_url == "https://example.com"
        assert p.api_key_env == "KEY"

    def test_optional_headers_default_none(self) -> None:
        p = ProviderConfig(name="T", base_url="u", api_key_env="K")
        assert p.extra_headers is None
        assert p.extra_body is None


# ---------------------------------------------------------------------------
# get_model_config()
# ---------------------------------------------------------------------------

class TestGetModelConfig:
    def test_known_model(self) -> None:
        cfg = get_model_config("deepseek-reasoner")
        assert cfg is not None
        assert cfg.name == "deepseek-reasoner"
        assert cfg.provider == "deepseek"

    def test_openrouter_model(self) -> None:
        cfg = get_model_config("anthropic/claude-sonnet-4")
        assert cfg is not None
        assert cfg.provider == "openrouter"

    def test_unknown_model_returns_none(self) -> None:
        assert get_model_config("nonexistent-model-999") is None

    def test_empty_string_returns_none(self) -> None:
        assert get_model_config("") is None

    @pytest.mark.parametrize("model_name", list(MODELS.keys()))
    def test_all_registered_models_resolve(self, model_name: str) -> None:
        cfg = get_model_config(model_name)
        assert cfg is not None
        assert cfg.name == model_name


# ---------------------------------------------------------------------------
# get_provider_config()
# ---------------------------------------------------------------------------

class TestGetProviderConfig:
    def test_deepseek_provider(self) -> None:
        cfg = get_provider_config("deepseek")
        assert cfg is not None
        assert cfg.name == "DeepSeek"
        assert "deepseek" in cfg.base_url

    def test_openrouter_provider(self) -> None:
        cfg = get_provider_config("openrouter")
        assert cfg is not None
        assert "openrouter" in cfg.base_url

    def test_mcp_provider(self) -> None:
        cfg = get_provider_config("mcp")
        assert cfg is not None
        assert cfg.api_key_env == ""

    def test_unknown_provider_returns_none(self) -> None:
        assert get_provider_config("azure") is None

    @pytest.mark.parametrize("provider_name", list(PROVIDERS.keys()))
    def test_all_registered_providers_resolve(self, provider_name: str) -> None:
        cfg = get_provider_config(provider_name)
        assert cfg is not None
        assert cfg.name  # non-empty display name


# ---------------------------------------------------------------------------
# is_valid_model()
# ---------------------------------------------------------------------------

class TestIsValidModel:
    @pytest.mark.parametrize("model_name", list(MODELS.keys()))
    def test_registered_models_are_valid(self, model_name: str) -> None:
        assert is_valid_model(model_name) is True

    @pytest.mark.parametrize(
        "model_name",
        ["", "fake-model", "gpt-5", "deepseek", "openrouter"],
    )
    def test_invalid_models(self, model_name: str) -> None:
        assert is_valid_model(model_name) is False


# ---------------------------------------------------------------------------
# get_models_by_provider()
# ---------------------------------------------------------------------------

class TestGetModelsByProvider:
    def test_deepseek_models(self) -> None:
        models = get_models_by_provider("deepseek")
        assert len(models) >= 1
        assert all(m.provider == "deepseek" for m in models)

    def test_openrouter_models(self) -> None:
        models = get_models_by_provider("openrouter")
        assert len(models) >= 1
        assert all(m.provider == "openrouter" for m in models)

    def test_unknown_provider_returns_empty(self) -> None:
        assert get_models_by_provider("nonexistent") == []


# ---------------------------------------------------------------------------
# get_all_models()
# ---------------------------------------------------------------------------

class TestGetAllModels:
    def test_returns_all_models(self) -> None:
        all_models = get_all_models()
        assert len(all_models) == len(MODELS)

    def test_returns_model_config_instances(self) -> None:
        for m in get_all_models():
            assert isinstance(m, ModelConfig)


# ---------------------------------------------------------------------------
# DEFAULT_MODEL
# ---------------------------------------------------------------------------

class TestDefaultModel:
    def test_default_is_valid(self) -> None:
        assert is_valid_model(DEFAULT_MODEL)

    def test_default_has_provider(self) -> None:
        cfg = get_model_config(DEFAULT_MODEL)
        assert cfg is not None
        assert get_provider_config(cfg.provider) is not None


# ---------------------------------------------------------------------------
# Cross-checks — every model references a valid provider
# ---------------------------------------------------------------------------

class TestRegistryIntegrity:
    @pytest.mark.parametrize("model_name", list(MODELS.keys()))
    def test_model_provider_exists(self, model_name: str) -> None:
        cfg = get_model_config(model_name)
        assert cfg is not None
        provider = get_provider_config(cfg.provider)
        assert provider is not None, f"model '{model_name}' references unknown provider '{cfg.provider}'"

    def test_no_duplicate_model_names(self) -> None:
        names = [m.name for m in get_all_models()]
        assert len(names) == len(set(names))
