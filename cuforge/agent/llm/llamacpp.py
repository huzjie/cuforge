# -*- coding: utf-8 -*-
"""LlamaCppBackend：llama.cpp server 后端（OpenAI 兼容协议）。"""
from __future__ import annotations

from .openai_compat import OpenAICompatBackend


class LlamaCppBackend(OpenAICompatBackend):
    name = "llamacpp"

    def __init__(self, model: str, base_url: str = "http://localhost:8080/v1",
                 api_key: str = "none", **kwargs) -> None:
        super().__init__(model, base_url=base_url, api_key=api_key, **kwargs)
