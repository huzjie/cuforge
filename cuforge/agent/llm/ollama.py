# -*- coding: utf-8 -*-
"""OllamaBackend：本地 Ollama 后端（OpenAI 兼容协议）。"""
from __future__ import annotations

from .openai_compat import OpenAICompatBackend


class OllamaBackend(OpenAICompatBackend):
    name = "ollama"

    def __init__(self, model: str, base_url: str = "http://localhost:11434/v1",
                 api_key: str = "ollama", **kwargs) -> None:
        super().__init__(model, base_url=base_url, api_key=api_key, **kwargs)
