# -*- coding: utf-8 -*-
"""LLM 后端工厂。"""
from __future__ import annotations

from typing import Any, Dict

from .base import LLMBackend
from .mock import MockBackend
from .openai_compat import OpenAICompatBackend
from .vllm import VLLMBackend


def build_backend(cfg: Dict[str, Any] | Any) -> LLMBackend:
    """按配置构建 LLM 后端。cfg 可为 dict 或 LlmConfig dataclass。"""
    if hasattr(cfg, "provider"):
        provider = cfg.provider
        model = cfg.model
        base_url = getattr(cfg, "base_url", "")
        api_key = getattr(cfg, "api_key", "")
    else:
        provider = cfg.get("provider", "mock")
        model = cfg.get("model", "qwen3.5-9b")
        base_url = cfg.get("base_url", "")
        api_key = cfg.get("api_key", "")

    if provider == "openai_compat":
        return OpenAICompatBackend(model, base_url=base_url, api_key=api_key)
    if provider == "vllm":
        return VLLMBackend(model, base_url=base_url or "http://localhost:8000/v1",
                           api_key=api_key or "EMPTY")
    return MockBackend(model)
