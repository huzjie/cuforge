# -*- coding: utf-8 -*-
"""扩展后端工厂：支持全部内置 + 扩展后端。"""
from __future__ import annotations

from typing import Any, Dict

from .anthropic import AnthropicBackend
from .base import LLMBackend
from .gemini import GeminiBackend
from .llamacpp import LlamaCppBackend
from .ollama import OllamaBackend
from .sglang import SGLangBackend
from .tokenspeed import TokenSpeedBackend

BACKENDS = {
    "anthropic": AnthropicBackend,
    "gemini": GeminiBackend,
    "ollama": OllamaBackend,
    "llamacpp": LlamaCppBackend,
    "sglang": SGLangBackend,
    "tokenspeed": TokenSpeedBackend,
}


def build_backend_ext(cfg: Dict[str, Any]) -> LLMBackend:
    provider = cfg.get("provider", "mock")
    model = cfg.get("model", "qwen3.5-9b")
    if provider in BACKENDS:
        cls = BACKENDS[provider]
        if provider in ("anthropic", "gemini"):
            return cls(model, api_key=cfg.get("api_key", ""))
        return cls(model, base_url=cfg.get("base_url", ""), api_key=cfg.get("api_key", ""))
    from .registry import build_backend
    return build_backend(cfg)
